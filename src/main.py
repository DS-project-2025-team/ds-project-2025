import logging

from entities.server_address import ServerAddress
from raft.node import Node
from raft.roles.role import Role
from services.logger_service import logger


async def main(
    role: Role,
    server: ServerAddress,
    log_level: str,
) -> None:
    level = getattr(logging, log_level.upper())
    logger.set_level(level)

    async with Node(server=server, role=role) as node:
        await node.run()
