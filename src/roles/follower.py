import random
from time import sleep
from typing import Literal

from roles.role import Role
from services.logger_service import logger


class Follower:
    def __init__(self, election_timeout: int | None) -> None:
        self.__election_timeout = election_timeout or 1000 + random.randint(0, 1000)

    def run(self) -> Literal[Role.CANDIDATE]:
        sleep(self.__election_timeout / 1000)

        logger.info("Changing role to CANDIDATE")
        return Role.CANDIDATE
