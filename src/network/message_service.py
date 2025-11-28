import json
from contextlib import AbstractAsyncContextManager
from types import TracebackType
from typing import Self

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer


def serializer(value: dict) -> bytes:
    return json.dumps(value).encode()


def deserializer(serialized: str) -> dict:
    return json.loads(serialized)


class MessageService(AbstractAsyncContextManager):
    def __init__(
        self,
        server: str,
        port: int = 9092,
    ) -> None:
        self.__producer: AIOKafkaProducer = AIOKafkaProducer(
            bootstrap_servers=f"{server}:{port}",
            value_serializer=serializer,
        )
        self.__consumer: AIOKafkaConsumer = AIOKafkaConsumer(
            bootstrap_servers=f"{server}:{port}",
            value_deserializer=deserializer,
        )

    async def send(self, topic: str, payload: dict) -> None:
        await self.__producer.send_and_wait(topic, payload)

    async def receive(self) -> dict:
        message = await self.__consumer.getmany()

        return message # type: ignore

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
