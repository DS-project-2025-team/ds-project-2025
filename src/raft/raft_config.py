import asyncio
from uuid import UUID

from entities.server_address import ServerAddress
from services.logger_service import logger


class RaftConfig:
    def __init__(
            self,
            nodes: list[tuple[UUID, ServerAddress]] | None=None,
            count: int = 0
    ) -> None:
        self.nodes: list[tuple[UUID, ServerAddress]] = []
        self.lock: asyncio.Lock = asyncio.Lock()
        self.count = count

    async def add_node(self, uuid: UUID, server: ServerAddress) -> None:
        async with asyncio.Lock():
            data: tuple[UUID, ServerAddress] = (uuid, server)
            self.nodes.append(data)
            self.count += 1

        logger.debug("RaftConfig: added node: %s", data)

    def get_config_nodes(self) -> list:
        return self.nodes

    def get_config_nodecount(self) -> int:
        return self.count
