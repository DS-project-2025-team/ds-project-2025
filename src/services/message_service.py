from contextlib import AbstractAsyncContextManager
from types import TracebackType
from typing import Self

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer


class MessageService(AbstractAsyncContextManager):
    def __init__(
        self,
        server: str,
        port: int = 9092,
    ) -> None:
        self.__producer: AIOKafkaProducer = AIOKafkaProducer(
            bootstrap_servers=f"{server}:{port}"
        )
        self.__consumer: AIOKafkaConsumer = AIOKafkaConsumer(
            bootstrap_servers=f"{server}:{port}"
        )

    async def send(self, topic: str, message: bytes) -> None:
        await self.__producer.send_and_wait(topic, message)

    async def receive(self) -> str:
        message = await self.__consumer.getone()

        return str(message.value)

    async def subscribe(self, *topics: str) -> None:
        """
        Override currently subscribed topics.
        """

        self.__consumer.subscribe(topics)

    async def __aenter__(self) -> Self:
        await self.__producer.start()
        await self.__consumer.start()

        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.__producer.stop()
        await self.__consumer.stop()
