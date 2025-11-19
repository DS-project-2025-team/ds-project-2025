from typing import Literal

from roles.role import Role
from services.logger_service import logger


class Leader:
    def run(self) -> Literal[Role.FOLLOWER]:
        logger.info("Changing role to FOLLOWER")
        return Role.FOLLOWER
