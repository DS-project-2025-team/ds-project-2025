from logging import getLogger
from typing import Literal

from roles.role import Role

logger = getLogger(__name__)


class Leader:
    def run(self) -> Literal[Role.FOLLOWER]:
        logger.info("Changing role to FOLLOWER")
        return Role.FOLLOWER
