import asyncio
from contextlib import AbstractAsyncContextManager, suppress
from types import TracebackType
from typing import Self
from uuid import UUID

from entities.second import Second
from entities.server_address import ServerAddress
from network.message_consumer import MessageConsumer
from network.message_consumer_factory import MessageConsumerFactory
from network.message_producer import MessageProducer
from network.topic import Topic
from utils.async_loop import async_loop


class PingService(AbstractAsyncContextManager):
    """
    Class for counting alive consumers, assuming one consumer per group.
    """

    def __init__(
        self,
        server: ServerAddress,
        node_id: UUID,
        producer: MessageProducer,
        count: int = 0,
        timeout: Second = Second(5),
    ) -> None:
        self.__count: int = count
        self.__id: UUID = node_id
        self.__timeout: Second = timeout
        self.__producer: MessageProducer = producer
        self.__consumer: MessageConsumer = (
            MessageConsumerFactory.ping_response_consumer(server, node_id)
        )

    async def __aenter__(self) -> Self:
        self.__consumer = await self.__consumer.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        await self.__consumer.__aexit__(exc_type, exc_value, traceback)

    async def count_consumers(self) -> int:
        """
        Counts alive consumers.

        Returns:
            int: Number of alive consumers
        """
        payload = {
            "sender": str(self.__id),
        }

        await self.__producer.send(Topic.PING, payload)

        with suppress(TimeoutError):
            await asyncio.wait_for(self.receive_response(), timeout=self.__timeout)

        return self.__count

    @async_loop
    async def receive_response(self) -> None:
        message = await self.__consumer.receive()

        if message.data["receiver"] != self.__id:
            return

        async with asyncio.Lock():
            self.__count += 1
