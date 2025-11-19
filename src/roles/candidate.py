from logging import getLogger
from typing import Literal

from roles.role import Role

logger = getLogger(__name__)


class Candidate:
    @staticmethod
    def elect() -> Literal[Role.LEADER, Role.CANDIDATE]:
        logger.info("Changing role to LEADER")
        return Role.LEADER
