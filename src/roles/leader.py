from collections import deque
from typing import Literal

from entities.raft_log import RaftLog
from roles.role import Role
from services.logger_service import logger
from services.message_service import MessageService


class Leader:
    def __init__(
        self,
        message_service: MessageService,
        log: RaftLog,
        queue: deque[int] | None = None,
    ) -> None:
        self.__message_service = message_service
        self.__queue: deque[int] = queue or deque()
        self.__log = log

    def run(self) -> Literal[Role.FOLLOWER]:
        logger.info("Changing role to FOLLOWER")
        return Role.FOLLOWER
