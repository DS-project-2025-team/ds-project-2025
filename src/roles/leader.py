import asyncio
from collections import deque
from contextlib import AbstractAsyncContextManager, suppress
from types import TracebackType
from typing import Literal, Self
from uuid import UUID

from entities.log_entry_factory import LogEntryFactory
from entities.raft_log import RaftLog
from entities.sat_formula import SatFormula
from entities.second import Second
from entities.server_address import ServerAddress
from logger_service import logger
from network.message import Message
from network.message_consumer import MessageConsumer
from network.message_consumer_factory import MessageConsumerFactory
from network.message_producer import MessageProducer
from network.topic import Topic
from roles.role import Role
from utils.async_loop import async_loop


class Leader(AbstractAsyncContextManager):
    def __init__(
        self,
        log: RaftLog,
        server: ServerAddress,
        node_id: UUID,
        queue: deque[int] | None = None,
    ) -> None:
        self.__producer: MessageProducer = MessageProducer(server=server)
        self.__input_consumer: MessageConsumer = MessageConsumerFactory.input_consumer(
            server,
            node_id,
        )
        self.__heartbeat_consumer: MessageConsumer = (
            MessageConsumerFactory.heartbeat_response_consumer(
                server=server, node_id=node_id
            )
        )

        self.__tasks: deque[int] = queue or deque()
        self.__log: RaftLog = log
        self.__node_id = node_id

    async def __aenter__(self) -> Self:
        await self.__producer.__aenter__()
        await self.__input_consumer.__aenter__()
        await self.__heartbeat_consumer.__aenter__()  # heartbeat response

        self.__running = True
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.__heartbeat_consumer.__aexit__(exc_type, exc_value, traceback)
        await self.__producer.__aexit__(exc_type, exc_value, traceback)
        await self.__input_consumer.__aexit__(exc_type, exc_value, traceback)

    # Leader main
    async def run(self) -> Literal[Role.FOLLOWER]:
        async with asyncio.TaskGroup() as group:
            group.create_task(self.__consume_loop())
            group.create_task(self.__send_heartbeat())
            group.create_task(self.__handle_input(Second(1)))

        logger.info("Changing role to FOLLOWER")
        return Role.FOLLOWER

    @async_loop
    async def __handle_input(self, timeout: Second) -> None:
        with suppress(TimeoutError):
            message = await self.__input_consumer.receive(timeout)

            input_ = message.data

            formula = SatFormula(input_["data"])
            logger.info(f"Received new SAT formula: {formula}")

    @async_loop
    async def __send_heartbeat(self) -> None:
        await self.__producer.send_and_wait(
            Topic.HEARTBEAT, {"sender": str(self.__node_id)}
        )

        logger.debug(f"Sent {Topic.HEARTBEAT}")

    @async_loop
    async def __consume_loop(self) -> None:
        """
        Read messages via heartbeat_response_consumer
        """

        logger.info("Leader consumer loop started")

        message = await self.__heartbeat_consumer.receive()
        await self.__handle_message(message)

    async def __handle_message(self, message: Message) -> None:
        logger.debug(f"Received {message.topic}")

    def __next_task(self) -> int | None:
        task = None

        while self.__tasks:
            task = self.__tasks.popleft()

            if not self.__log.completed_tasks[task]:
                self.__tasks.append(task)
                break

        return task

    def __complete_task(self, task: int) -> None:
        entry = LogEntryFactory.complete_task(self.__log.term, task)

        self.__log.append(entry)
        self.__log.commit()

    async def __receive_input(self, timeout: Second) -> SatFormula | None:
        try:
            message = await self.__input_consumer.receive(timeout)
            input_ = message.data
        except TimeoutError:
            return None

        formula = SatFormula(input_["data"])
        logger.info(f"Received new SAT formula: {formula}")
