import asyncio
import random
from contextlib import AbstractAsyncContextManager
from types import TracebackType
from typing import Literal, Self
from uuid import uuid4

from logger_service import logger
from network.message_consumer import MessageConsumer
from network.topic import Topic
from roles.role import Role


class Follower(AbstractAsyncContextManager):
    def __init__(
        self, server: str, port: int, election_timeout: int | None = None
    ) -> None:
        self.__heartbeat_consumer = MessageConsumer(
            Topic.HEARTBEAT, server=server, port=port, groupid=str(uuid4())
        )
        self.__election_timeout = election_timeout or 1000 + random.randint(0, 1000)

    async def __aenter__(self) -> Self:
        await self.__heartbeat_consumer.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.__heartbeat_consumer.__aexit__(exc_type, exc_value, traceback)

    async def run(self) -> Literal[Role.CANDIDATE]:
        while True:
            try:
                message = await asyncio.wait_for(
                    self.__heartbeat_consumer.receive(),
                    self.__election_timeout / 1000.0,
                )
                logger.info("Received heartbeat", message)

            except TimeoutError:
                break

            self.__process_message(message)

        logger.info("Changing role to CANDIDATE")
        return Role.CANDIDATE

    def __process_message(self, message: dict) -> None:
        match message["topic"]:
            case Topic.HEARTBEAT:
                logger.debug("Received heartbeat from leader")
