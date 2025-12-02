import asyncio
import random
from contextlib import AbstractAsyncContextManager
from types import TracebackType
from typing import Literal, Self
from uuid import UUID

from entities.second import Second
from entities.server_address import ServerAddress
from logger_service import logger
from network.message_consumer import MessageConsumer
from network.message_consumer_factory import MessageConsumerFactory
from roles.role import Role


class Follower(AbstractAsyncContextManager):
    def __init__(
        self,
        server: ServerAddress,
        node_id: UUID,
        election_timeout: Second | None = None,
    ) -> None:
        self.__heartbeat_consumer: MessageConsumer = (
            MessageConsumerFactory.heartbeat_consumer(server=server, node_id=node_id)
        )
        self.__election_timeout: Second = election_timeout or Second(
            10 + random.randint(0, 5)
        )

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
                    self.__election_timeout,
                )
                logger.info("Received heartbeat")

            except TimeoutError:
                logger.warning("Missing heartbeat, election timeout elapsed.")
                break

            self.__process_message(message)

        logger.info("Changing role to CANDIDATE")
        return Role.CANDIDATE

    def __process_message(self, message: dict) -> None:
        pass
