import json
from contextlib import AbstractAsyncContextManager
from types import TracebackType
from typing import Self

from aiokafka import AIOKafkaConsumer

from logger_service import logger


def deserializer(serialized: str) -> dict:
    return json.loads(serialized)


class MessageConsumer(AbstractAsyncContextManager):
    def __init__(
        self, *topics: str, server: str, port: int = 9092, groupid: str | None = None
    ) -> None:
        self.__consumer: AIOKafkaConsumer = AIOKafkaConsumer(
            *topics,
            group_id=groupid,
            bootstrap_servers=f"{server}:{port}",
            value_deserializer=deserializer,
            auto_offset_reset="earliest",
        )

    async def commit(self) -> None:
        await self.__consumer.commit()

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
