import asyncio
from contextlib import AbstractAsyncContextManager
from types import TracebackType
from typing import Self
from uuid import UUID

from entities.raft_log import RaftLog
from entities.second import Second
from entities.server_address import ServerAddress
from error import LeaderExistsError, OutDatedTermError
from network.message_consumer import MessageConsumer
from network.message_consumer_factory import MessageConsumerFactory
from network.message_producer import MessageProducer
from network.topic import Topic
from raft.role import Role
from services.logger_service import logger
from services.ping_service import PingService
from utils.async_loop import async_loop


class SufficientVotes(Exception):  # noqa: N818
    pass


class Candidate(AbstractAsyncContextManager):
    def __init__(
        self,
        server: ServerAddress,
        log: RaftLog,
        node_id: UUID,
        vote_timeout: Second = Second(20),
    ) -> None:
        self.__id = node_id
        self.__vote_timeout = vote_timeout

        self.__log: RaftLog = log

        self.__ping_service: PingService = PingService(server=server, node_id=node_id)
        self.__producer = MessageProducer(server=server)
        self.__vote_consumer = MessageConsumerFactory.vote_consumer(
            server=server, node_id=node_id
        )
        self.__appendentry_consumer: MessageConsumer = (
            MessageConsumerFactory.appendentry_consumer(server=server, node_id=node_id)
        )

    async def __aenter__(self) -> Self:
        await self.__ping_service.__aenter__()
        await self.__producer.__aenter__()
        await self.__vote_consumer.__aenter__()
        await self.__appendentry_consumer.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.__ping_service.__aexit__(exc_type, exc_value, traceback)
        await self.__producer.__aexit__(exc_type, exc_value, traceback)
        await self.__vote_consumer.__aexit__(exc_type, exc_value, traceback)
        await self.__appendentry_consumer.__aexit__(exc_type, exc_value, traceback)

    async def run(self) -> Role:
        term = self.__log.term + 1
        nodes = await self.__count_nodes()

        role = Role.FOLLOWER

        try:
            await asyncio.create_task(self.__check_leader_existence(term))

            role = await asyncio.wait_for(
                self.__elect(term, nodes), timeout=self.__vote_timeout
            )

        except (LeaderExistsError, OutDatedTermError) as error:
            logger.info(str(error))

        except TimeoutError:
            logger.info(f"Election for term {term} timed out.")
            role = Role.CANDIDATE

        return role

    async def __elect(self, term: int, nodes: int) -> Role:
        logger.info(f"Starting election for term {term}")

        await self.__send_vote_request(term)
        await self.__wait_for_votes(term, nodes)

        return Role.LEADER

    async def __send_vote_request(self, term: int) -> None:
        last_log_index = self.__log.last_log_index
        last_log_term = self.__log.last_log_term

        payload = {
            "term": term,
            "candidate_id": self.__id,
            "last_log_index": last_log_index,
            "last_log_term": last_log_term,
        }

        await self.__producer.send(Topic.VOTE_REQUEST, payload)
        logger.info("Sent vote requests")

    async def __wait_for_votes(self, term: int, nodes: int) -> None:
        votes = 0
        votes_required = nodes // 2 + 1

        while votes < votes_required:
            votes += await self.__receive_vote(term)

    async def __count_nodes(self) -> int:
        return await self.__ping_service.count_consumers()

    async def __receive_vote(self, term: int) -> int:
        message = await self.__vote_consumer.receive()

        vote_term = message.data["term"]
        vote_granted = message.data["vote_granted"]

        if vote_term > term:
            self.__log.term = vote_term
            raise OutDatedTermError(term, vote_term)

        if not vote_granted:
            return 0

        return 1

    @async_loop
    async def __check_leader_existence(self, term: int) -> None:
        message = await self.__appendentry_consumer.receive()

        leader_term = message.data["term"]

        if leader_term >= term:
            raise LeaderExistsError()
