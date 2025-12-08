import asyncio
from contextlib import AbstractAsyncContextManager
from types import TracebackType
from typing import Self
from uuid import UUID

from entities.second import Second
from entities.server_address import ServerAddress
from error import LeaderExistsError, OutDatedTermError
from network.message_consumer import MessageConsumer
from network.message_consumer_factory import MessageConsumerFactory
from network.message_producer import MessageProducer
from network.topic import Topic
from raft.entities.log import Log
from raft.roles.role import Role
from services.logger_service import logger
from services.ping_service import PingService
from utils.async_loop import async_loop


class Candidate(AbstractAsyncContextManager):
    def __init__(
        self,
        server: ServerAddress,
        log: Log,
        node_id: UUID,
        producer: MessageProducer,
        vote_timeout: Second = Second(20),
    ) -> None:
        self.__id: UUID = node_id
        self.__vote_timeout: Second = vote_timeout

        self.__log: Log = log

        self.__ping_service: PingService = PingService(
            server=server, node_id=node_id, producer=producer
        )
        self.__producer: MessageProducer = producer
        self.__vote_consumer: MessageConsumer = MessageConsumerFactory.vote_consumer(
            server=server, node_id=node_id
        )
        self.__appendentry_consumer: MessageConsumer = (
            MessageConsumerFactory.appendentry_consumer(server=server, node_id=node_id)
        )

    async def __aenter__(self) -> Self:
        await self.__ping_service.__aenter__()
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
        await self.__vote_consumer.__aexit__(exc_type, exc_value, traceback)
        await self.__appendentry_consumer.__aexit__(exc_type, exc_value, traceback)

    @property
    def term(self) -> int:
        return self.__log.term

    async def run(self) -> Role:
        self.__log.term += 1
        logger.info(f"Canditate running for term {self.term}")

        nodes = await self.__count_nodes()

        role = Role.FOLLOWER

        try:
            await asyncio.create_task(self.__check_leader_existence())

            role = await asyncio.wait_for(
                self.__elect(nodes), timeout=self.__vote_timeout
            )

        except (LeaderExistsError, OutDatedTermError) as error:
            logger.info(str(error))

        except TimeoutError:
            logger.info(f"Election for term {self.term} timed out.")
            role = Role.CANDIDATE

        return role

    async def __elect(self, nodes: int) -> Role:
        logger.info(f"Starting election for term {self.term}")

        await self.__send_vote_request()
        await self.__wait_for_votes(nodes)

        return Role.LEADER

    async def __send_vote_request(self) -> None:
        last_log_index = self.__log.last_log_index
        last_log_term = self.__log.last_log_term

        payload = {
            "term": self.term,
            "candidate_id": self.__id,
            "last_log_index": last_log_index,
            "last_log_term": last_log_term,
        }

        await self.__producer.send(Topic.VOTE_REQUEST, payload)
        logger.info("Sent vote requests")

    async def __wait_for_votes(self, nodes: int) -> None:
        votes = 1
        votes_required = nodes // 2 + 1

        while votes < votes_required:
            votes += await self.__receive_vote()

    async def __count_nodes(self) -> int:
        count = await self.__ping_service.count_consumers()
        logger.info(f"Alive nodes: {count}")

        return count

    async def __receive_vote(self) -> int:
        message = await self.__vote_consumer.receive()

        vote_term = message.data["term"]
        vote_granted = message.data["vote_granted"]

        if vote_term > self.term:
            old_term = self.term
            self.__log.term = vote_term

            raise OutDatedTermError(old_term, vote_term)

        if not vote_granted:
            return 0

        return 1

    @async_loop
    async def __check_leader_existence(self) -> None:
        message = await self.__appendentry_consumer.receive()

        leader_term = message.data["term"]

        if leader_term >= self.term:
            raise LeaderExistsError()
