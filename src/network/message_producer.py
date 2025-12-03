import json
from contextlib import AbstractAsyncContextManager
from types import TracebackType
from typing import Any, Self

from aiokafka import AIOKafkaProducer
from aiokafka.structs import RecordMetadata

from entities.server_address import ServerAddress
from logger_service import logger
from network.topic import Topic


def serializer(value: dict) -> bytes:
    return json.dumps(value).encode()


class MessageProducer(AbstractAsyncContextManager):
    def __init__(self, server: ServerAddress) -> None:
        self.__producer: AIOKafkaProducer = AIOKafkaProducer(
            bootstrap_servers=f"{server.host}:{server.port}",
            value_serializer=serializer,
        )

    async def send(self, topic: Topic, payload: dict[str, Any]) -> None:
        await self.__producer.send(topic, payload)
        logger.debug(
            'Sent message "%s": %r',
            topic,
            payload,
        )
        logger.debug('Sent "%s"', topic)

    async def send_and_wait(self, topic: Topic, payload: dict) -> None:
        metadata: RecordMetadata = await self.__producer.send_and_wait(topic, payload)
        logger.debug(
            'Sent message "%s": %r (partition=%s offset=%s)',
            topic,
            payload,
            metadata.partition,
            metadata.offset,
        )

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
