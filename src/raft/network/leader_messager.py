from asyncio import TaskGroup
from collections.abc import Iterable
from contextlib import AbstractAsyncContextManager
from types import TracebackType
from typing import Self
from uuid import UUID

from entities.sat_formula import SatFormula
from entities.second import Second
from entities.server_address import ServerAddress
from network.message_consumer import MessageConsumer
from network.message_consumer_factory import MessageConsumerFactory
from network.message_producer import MessageProducer
from network.topic import Topic
from raft.entities.log_entry import LogEntry
from services.logger_service import logger


class LeaderMessager(AbstractAsyncContextManager):
    """
    Class for handling Leader messaging.
    """

    def __init__(
        self,
        server: ServerAddress,
        node_id: UUID,
        producer: MessageProducer,
        term: int,
    ) -> None:
        self.__producer: MessageProducer = producer
        self.__input_consumer: MessageConsumer = MessageConsumerFactory.input_consumer(
            server,
        )
        self.__append_entries_consumer: MessageConsumer = (
            MessageConsumerFactory.append_entries_response_consumer(
                server=server, node_id=node_id
            )
        )
        self.__report_consumer: MessageConsumer = (
            MessageConsumerFactory.report_consumer(server=server)
        )

        self.__id: UUID = node_id
        self.__term: int = term

    async def __aenter__(self) -> Self:
        async with TaskGroup() as group:
            _task1 = group.create_task(self.__input_consumer.__aenter__())
            _task2 = group.create_task(self.__append_entries_consumer.__aenter__())
            _task3 = group.create_task(self.__report_consumer.__aenter__())

        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        async with TaskGroup() as group:
            _task1 = group.create_task(
                self.__input_consumer.__aexit__(exc_type, exc_value, traceback)
            )
            _task2 = group.create_task(
                self.__append_entries_consumer.__aexit__(exc_type, exc_value, traceback)
            )
            _task3 = group.create_task(
                self.__report_consumer.__aexit__(exc_type, exc_value, traceback)
            )

    async def send_append_entries(
        self,
        entries: Iterable[LogEntry],
    ) -> None:
        await self.__producer.send(
            Topic.APPEND_ENTRIES,
            {
                "term": self.__term,
                "sender": str(self.__id),
                "entries": [entry.to_dict() for entry in entries],
            },
        )

    async def send_output(self, result: bool, hash_: int) -> None:
        payload = {
            "hash": hash_,
            "result": result,
        }

        await self.__producer.send(Topic.OUTPUT, payload)

    async def send_task(self, formula: SatFormula, task: int, exponent: int) -> None:
        payload = {"formula": formula.to_list(), "task": task, "exponent": exponent}

        await self.__producer.send(Topic.ASSIGN, payload)

    async def receive_input(self, timeout: Second) -> SatFormula:
        """
        Receives one SAT formula.

        Raises:
            TimeoutError: If timeout is exceeded.
        """

        message = await self.__input_consumer.receive(timeout)
        input_ = message.data

        return SatFormula(input_["data"])

    async def receive_report(self, hash_: int) -> tuple[int, bool] | None:
        message = await self.__report_consumer.receive()

        data = message.data

        if data["hash"] != hash_:
            logger.debug(f"Received outdated REPORT with hash {data['hash']}")
            return None

        task: int = data["task"]
        satisfiable: bool = message.data["result"]

        return task, satisfiable
