from typing import Literal

from logger_service import logger
from roles.role import Role


class Candidate:
    @staticmethod
    def elect() -> Literal[Role.LEADER, Role.CANDIDATE]:
        logger.info("Changing role to LEADER")
        return Role.LEADER
