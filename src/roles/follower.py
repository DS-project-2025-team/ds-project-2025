import random
from typing import Literal
import asyncio

from logger_service import logger
from network.message_service import MessageService
from roles.role import Role


class Follower:
    def __init__(
        self, message_service: MessageService, election_timeout: int | None = None
    ) -> None:
        self.__message_service = message_service
        self.__election_timeout = election_timeout or 1000 + random.randint(0, 1000)

    async def run(self) -> Literal[Role.CANDIDATE, Role.FOLLOWER]:
        try:
            msg = await asyncio.wait_for(
                self.__message_service.receive(), self.__election_timeout / 1000
            )

            if msg.get("type") == "heartbeat":
                logger.debug("Received heartbeat from leader")
                return Role.FOLLOWER

            return Role.FOLLOWER

        except asyncio.TimeoutError:
            logger.info("Changing role to CANDIDATE")
            return Role.CANDIDATE
