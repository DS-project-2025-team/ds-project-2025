from asyncio import TaskGroup
from contextlib import AbstractAsyncContextManager
from types import TracebackType
from typing import Self
from uuid import UUID

from entities.server_address import ServerAddress
from network.message_consumer import MessageConsumer
from network.message_consumer_factory import MessageConsumerFactory
from network.message_producer import MessageProducer


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
