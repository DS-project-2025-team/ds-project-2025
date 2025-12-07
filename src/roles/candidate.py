import asyncio
from contextlib import AbstractAsyncContextManager
from types import TracebackType
from typing import Self
from uuid import UUID

from entities.raft_log import RaftLog
from entities.second import Second
from entities.server_address import ServerAddress
from error import LeaderExistsError
from network.message_consumer import MessageConsumer
from network.message_consumer_factory import MessageConsumerFactory
from network.message_producer import MessageProducer
from network.topic import Topic
from roles.role import Role
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

        self.__term = log.term + 1

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

    async def elect(self) -> Role:
        logger.info(f"Starting election for term {self.__term}")

        begin_time = asyncio.get_event_loop().time()
        role = Role.FOLLOWER

        await self.__producer.send(Topic.VOTE_REQUEST, {})

        logger.info(f"{self.__id} sent vote requests to peers")

        try:
            async with asyncio.TaskGroup() as group:
                _task1 = group.create_task(self.__check_leader_existence())
                _task2 = group.create_task(self.__check_timeout(begin_time))
                _task3 = group.create_task(self.__check_votes())

        except LeaderExistsError:
            logger.info("Detected existing leader, aborting election.")

        except TimeoutError:
            logger.info("Election timed out.")
            role = Role.CANDIDATE

        except SufficientVotes:
            logger.info(f"Won the election for term {self.__term}")
            role = Role.LEADER

        return role

    async def __count_nodes(self) -> int:
        return await self.__ping_service.count_consumers()

    async def __receive_vote(self, current_term: int, timeout: float = 0.5) -> int:
        try:
            vote = await self.__vote_consumer.receive(Second(timeout))
        except TimeoutError:
            return 0

        return 1

    @async_loop
    async def __check_timeout(self, begin_time: float) -> None:
        if asyncio.get_event_loop().time() - begin_time > self.__vote_timeout:
            raise TimeoutError()

        await asyncio.sleep(1)

    @async_loop
    async def __check_leader_existence(self) -> bool:
        try:
            await self.__appendentry_consumer.receive(timeout=Second(1))

            logger.info("Detected existing leader via heartbeat")

            raise LeaderExistsError()

        except TimeoutError:
            return False

    async def __check_votes(self) -> None:
        self.__votes += await self.__receive_vote(self.__term)

        if self.__votes < self.__required_votes:
            return

        raise SufficientVotes()
