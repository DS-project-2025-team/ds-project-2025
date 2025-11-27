from typing import Literal

from roles.role import Role
from services.logger_service import logger
from services.message_service import MessageService


class Leader:
    def __init__(self, message_service: MessageService) -> None:
        self.__message_service = message_service

    def run(self) -> Literal[Role.FOLLOWER]:
        logger.info("Changing role to FOLLOWER")
        return Role.FOLLOWER
