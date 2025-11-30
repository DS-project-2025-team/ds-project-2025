import json
from contextlib import AbstractAsyncContextManager
from types import TracebackType
from typing import Any, Self

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from aiokafka.structs import RecordMetadata

from logger_service import logger


def serializer(value: dict) -> bytes:
    return json.dumps(value).encode()


def deserializer(serialized: str) -> dict:
    return json.loads(serialized)


class MessageService(AbstractAsyncContextManager):
    def __init__(self, server: str, port: int = 9092, groupid: str = "foo") -> None:
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

    async def send(self, topic: str, payload: dict[str, Any]) -> None:
        await self.__producer.send(topic, payload)

    async def send_and_wait(self, topic: str, payload: dict) -> RecordMetadata:
        assert self.__producer is not None
        metadata: RecordMetadata = await self.__producer.send_and_wait(topic, payload)
        logger.info(
            "Sent message to %s: %r (partition=%s offset=%s)",
            topic,
            payload,
            metadata.partition,
            metadata.offset,
        )
        return metadata

    async def receive(self) -> dict:
        messages = await self.__consumer.getmany()
        await self.__consumer.commit()
        for tp, msgs in messages.items():
            for msg in msgs:
                logger.info(
                    "Received message to %s: %r (partition=%s offset=%s)",
                    msg.topic,
                    msg.value,
                    msg.partition,
                    msg.offset,
                )

        return messages
        # return await self.__consumer.getmany()

    def subscribe(self, *topics: str) -> None:
        """
        Override currently subscribed topics.
        """

        self.__consumer.subscribe(topics)

    async def __aenter__(self) -> Self:
        await self.__producer.start()
        await self.__consumer.start()

        return self

    async def stop(self) -> None:
        await self.__producer.stop()
        await self.__consumer.stop()

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.__producer.stop()
        await self.__consumer.stop()
