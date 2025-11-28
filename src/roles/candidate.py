from typing import Literal

from roles.role import Role
from logger_service import logger


class Candidate:
    @staticmethod
    def elect() -> Literal[Role.LEADER, Role.CANDIDATE]:
        logger.info("Changing role to LEADER")
        return Role.LEADER
