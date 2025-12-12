from asyncio import TaskGroup
from contextlib import AbstractAsyncContextManager
from types import TracebackType
from typing import Self
from uuid import UUID

from entities.sat_formula import SatFormula
from entities.second import Second
from entities.server_address import ServerAddress
from network.message import Message
from network.message_consumer import MessageConsumer
from network.message_consumer_factory import MessageConsumerFactory
from network.message_producer import MessageProducer
from network.topic import Topic
from utils.hash_sat_formula import hash_sat_formula


class FollowerMessager(AbstractAsyncContextManager):
    def __init__(
        self,
        server: ServerAddress,
        producer: MessageProducer,
        node_id: UUID,
    ) -> None:
        self.__producer: MessageProducer = producer
        self.__append_entries_consumer: MessageConsumer = (
            MessageConsumerFactory.append_entries_consumer(
                server=server, node_id=node_id
            )
        )
        self.__assign_consumer: MessageConsumer = (
            MessageConsumerFactory.assign_consumer(server=server)
        )

        self.__id: UUID = node_id

    async def __aenter__(self) -> Self:
        async with TaskGroup() as group:
            _task1 = group.create_task(self.__append_entries_consumer.__aenter__())
            _task2 = group.create_task(self.__assign_consumer.__aenter__())

        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        async with TaskGroup() as group:
            _task1 = group.create_task(
                self.__append_entries_consumer.__aexit__(exc_type, exc_value, traceback)
            )
            _task2 = group.create_task(
                self.__assign_consumer.__aexit__(exc_type, exc_value, traceback)
            )

    async def send_report(self, formula: SatFormula, task: int, result: bool) -> None:
        payload = {
            "hash": hash_sat_formula(formula),
            "task": task,
            "result": result,
        }

        await self.__producer.send(Topic.REPORT, payload)

    async def send_append_entries_response(self, term: int) -> None:
        payload = {
            "responder_uuid": str(self.__id),
            "term": term,
        }

        await self.__producer.send(
            Topic.APPEND_ENTRIES_RESPONSE,
            payload,
        )

    async def receive_assign(self) -> tuple[SatFormula, int, int]:
        message = await self.__assign_consumer.receive()
        data = message.data

        formula: SatFormula = SatFormula(data["formula"])
        task: int = data["task"]
        exponent: int = data["exponent"]

        return formula, task, exponent

    async def receive_append_entries(self, election_timeout: Second) -> Message:
        message = await self.__append_entries_consumer.receive(election_timeout)
        await self.__append_entries_consumer.commit()

        return message
