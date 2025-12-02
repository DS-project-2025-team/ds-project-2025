import json
from contextlib import AbstractAsyncContextManager
from types import TracebackType
from typing import Self

from aiokafka import AIOKafkaConsumer

from entities.server_address import ServerAddress
from logger_service import logger


def deserializer(serialized: str) -> dict:
    return json.loads(serialized)


class MessageConsumer(AbstractAsyncContextManager):
    def __init__(
        self, *topics: str, server: ServerAddress, groupid: str | None = None
    ) -> None:
        self.__consumer: AIOKafkaConsumer = AIOKafkaConsumer(
            *topics,
            group_id=groupid,
            bootstrap_servers=f"{server.host}:{server.port}",
            value_deserializer=deserializer,
            auto_offset_reset="earliest",
        )

    async def commit(self) -> None:
        await self.__consumer.commit()

    async def receive(self) -> dict:
        message = await self.__consumer.getone()
        await self.__consumer.commit()
        logger.debug(
            "Received message to %s: %r (partition=%s offset=%s)",
            message.topic,
            message.value,
            message.partition,
            message.offset,
        )

        return message.value  # type: ignore

    async def receive_many_and_log(self) -> dict:
        messages = await self.__consumer.getmany()
        await self.__consumer.commit()
        for tp, msgs in messages.items():
            for msg in msgs:
                logger.debug(
                    "Received message to %s: %r (partition=%s offset=%s)",
                    msg.topic,
                    msg.value,
                    msg.partition,
                    msg.offset,
                )

        return messages

    async def __aenter__(self) -> Self:
        await self.__consumer.start()

        return self

    async def stop(self) -> None:
        await self.__consumer.stop()

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.__consumer.stop()
