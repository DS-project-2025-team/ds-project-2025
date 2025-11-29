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
        groupid: str = 'foo'
    ) -> None:
        self.__producer: AIOKafkaProducer = AIOKafkaProducer(
            bootstrap_servers=f"{server}:{port}",
            value_serializer=serializer,
        )
        self.__consumer: AIOKafkaConsumer = AIOKafkaConsumer(
            group_id=f"{groupid}",
            bootstrap_servers=f"{server}:{port}",
            value_deserializer=deserializer,
            auto_offset_reset="earliest",
        )

    async def commit(self) -> None:
        await self.__consumer.commit()

    async def send(self, topic: str, payload: dict) -> None:
        await self.__producer.send_and_wait(topic, payload)

    async def receive(self) -> dict:
        await self.__consumer.getmany()

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
