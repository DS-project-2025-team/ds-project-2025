import asyncio
from collections import deque
from contextlib import AbstractAsyncContextManager
from types import TracebackType
from typing import Literal, Self

from entities.leader_state import LeaderState
from entities.log_entry import LogEntry
from entities.raft_log import RaftLog
from entities.server_address import ServerAddress
from logger_service import logger
from network.message_consumer import MessageConsumer
from network.message_consumer_factory import MessageConsumerFactory
from network.message_producer import MessageProducer
from network.topic import Topic
from roles.role import Role


class Leader(AbstractAsyncContextManager):
    def __init__(
        self,
        log: RaftLog,
        server: ServerAddress,
        queue: deque[int] | None = None,
    ) -> None:
        self.__producer: MessageProducer = MessageProducer(server=server)
        self.__input_consumer: MessageConsumer = MessageConsumerFactory.input_consumer(
            server
        )
        self.__tasks: deque[int] = queue or deque()
        self.__log: RaftLog = log

    async def __aenter__(self) -> Self:
        await self.__producer.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.__producer.__aexit__(exc_type, exc_value, traceback)

    async def run(self) -> Literal[Role.FOLLOWER]:
        while True:
            await self.__producer.send_and_wait(Topic.HEARTBEAT, {})
            logger.info("Sent heartbeat")

            await asyncio.sleep(2)

        logger.info("Changing role to FOLLOWER")
        return Role.FOLLOWER

    def __next_task(self) -> int | None:
        task = None

        while self.__tasks:
            task = self.__tasks.popleft()

            if not self.__log.completed_tasks[task]:
                self.__tasks.append(task)
                break

        return task

    def __complete_task(self, task: int) -> None:
        entry = LogEntry(self.__log.term, lambda state: __complete_task(state, task))

        self.__log.append(entry)
        self.__log.commit()


def __complete_task(state: LeaderState, task: int) -> None:
    state.completed_tasks[task] = True
