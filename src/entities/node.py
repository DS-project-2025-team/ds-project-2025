from asyncio import TaskGroup
from uuid import UUID, uuid4

from entities.raft_log import RaftLog
from entities.server_address import ServerAddress
from roles.follower import Follower
from roles.leader import Leader
from roles.role import Role
from utils.async_loop import async_loop


class Node:
    def __init__(
        self,
        server: ServerAddress,
        node_id: UUID | None = None,
        peers: list[str] | None = None,
        role: Role = Role.FOLLOWER,
        log: RaftLog | None = None,
    ) -> None:
        self.node_id: UUID = node_id or uuid4()
        self.peers: list[str] = peers or []
        self.__server: ServerAddress = server
        self.__role: Role = role
        self.__log: RaftLog = log or RaftLog()

    @async_loop
    async def run(self) -> None:
        async with TaskGroup() as group:
            _task1 = group.create_task(self.__run_raft())

    @async_loop
    async def __run_raft(self) -> None:
        match self.__role:
            case Role.FOLLOWER:
                async with Follower(
                    server=self.__server, node_id=self.node_id
                ) as follower:
                    self.__role = await follower.run()

            case Role.CANDIDATE:
                # candidate = Candidate(self.__message_service, self.peers, self.__log)
                # self.__role = await candidate.elect()
                self.__role = Role.LEADER

            case Role.LEADER:
                async with Leader(
                    log=self.__log, server=self.__server, node_id=self.node_id
                ) as leader:
                    self.__role = await leader.run()
