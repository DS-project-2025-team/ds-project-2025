from contextlib import AbstractAsyncContextManager
from types import TracebackType
from typing import Any, Self
from uuid import UUID

from entities.server_address import ServerAddress
from network.message_consumer import MessageConsumer
from network.message_consumer_factory import MessageConsumerFactory
from network.message_producer import MessageProducer


class PingService(AbstractAsyncContextManager):
    """
    Class for counting alive consumers, assuming one consumer per group.
    """

    def __init__(
        self,
        server: ServerAddress,
        node_id: UUID,
        count: int = 0,
    ) -> None:
        self.__count: int = count
        self.__producer: MessageProducer = MessageProducer(server)
        self.__consumer: MessageConsumer = (
            MessageConsumerFactory.ping_response_consumer(server, node_id)
        )

    async def __aenter__(self) -> Self:
        self.__producer = await self.__producer.__aenter__()
        self.__consumer = await self.__consumer.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        await self.__producer.__aexit__(exc_type, exc_value, traceback)
        await self.__consumer.__aexit__(exc_type, exc_value, traceback)
