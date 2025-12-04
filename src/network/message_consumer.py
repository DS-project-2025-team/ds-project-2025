import asyncio
import json
from contextlib import AbstractAsyncContextManager, suppress
from types import TracebackType
from typing import Literal, Self

from aiokafka import AIOKafkaConsumer, IllegalOperation

from entities.second import Second
from entities.server_address import ServerAddress
from services.logger_service import logger
from network.message import Message


def deserializer(serialized: str) -> dict:
    return json.loads(serialized)


class MessageConsumer(AbstractAsyncContextManager):
    def __init__(
        self,
        *topics: str,
        server: ServerAddress,
        groupid: str,
        offset_reset: Literal["earliest", "latest"],
    ) -> None:
        self.__consumer: AIOKafkaConsumer = AIOKafkaConsumer(
            *topics,
            group_id=groupid,
            bootstrap_servers=f"{server.host}:{server.port}",
            value_deserializer=deserializer,
            auto_offset_reset=offset_reset,
        )

    async def commit(self) -> None:
        await self.__consumer.commit()

    async def receive(self, timeout: Second | None = None) -> Message:
        """
        Receives a message from message broker.

        Args:
            timeout (Second | None, optional): Timeout. Defaults to None.

        Returns:
            dict: Message payload

        Raises:
            TimeoutError: Timeout exceeded
        """

        message = Message.from_record(
            await asyncio.wait_for(self.__consumer.getone(), timeout=timeout)
        )

        with suppress(IllegalOperation):
            await self.__consumer.commit()

        logger.debug(
            f"Received message {message})",
        )

        return message

    async def receive_many_and_log(self) -> dict:
        messages = await self.__consumer.getmany()
        await self.__consumer.commit()
        for tp, msgs in messages.items():
            for msg in msgs:
                message = Message.from_record(msg)

                logger.debug(f"Received message {message}")

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
