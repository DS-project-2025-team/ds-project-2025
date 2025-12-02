from contextlib import AbstractAsyncContextManager
from types import TracebackType
from typing import Self

from entities.server_address import ServerAddress
from network.message_consumer import MessageConsumer
from network.message_producer import MessageProducer
from network.topic import Topic


class Client(AbstractAsyncContextManager):
    """
    Class for sending SAT formulas into the system and receiving the result.
    """

    def __init__(self, server: ServerAddress) -> None:
        self.__producer = MessageProducer(server)
        self.__consumer = MessageConsumer(Topic.OUTPUT, server=server)

    async def __aenter__(self) -> Self:
        await self.__consumer.__aenter__()
        await self.__producer.__aenter__()

        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.__producer.__aexit__(exc_type, exc_value, traceback)
        await self.__consumer.__aexit__(exc_type, exc_value, traceback)
