import json
from contextlib import AbstractAsyncContextManager
from types import TracebackType
from typing import Any, Self

from aiokafka import AIOKafkaProducer
from aiokafka.structs import RecordMetadata

from logger_service import logger


def serializer(value: dict) -> bytes:
    return json.dumps(value).encode()


class MessageProducer(AbstractAsyncContextManager):
    def __init__(self, server: str, port: int = 9092) -> None:
        self.__producer: AIOKafkaProducer = AIOKafkaProducer(
            bootstrap_servers=f"{server}:{port}",
            value_serializer=serializer,
        )

    async def send(self, topic: str, payload: dict[str, Any]) -> None:
        await self.__producer.send(topic, payload)

    async def send_and_wait(self, topic: str, payload: dict) -> RecordMetadata:
        metadata: RecordMetadata = await self.__producer.send_and_wait(topic, payload)
        logger.info(
            "Sent message to %s: %r (partition=%s offset=%s)",
            topic,
            payload,
            metadata.partition,
            metadata.offset,
        )
        return metadata

    async def __aenter__(self) -> Self:
        await self.__producer.start()

        return self

    async def stop(self) -> None:
        await self.__producer.stop()

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.__producer.stop()
