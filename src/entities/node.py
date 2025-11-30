from uuid import UUID, uuid4

from entities.raft_log import RaftLog
from roles.candidate import Candidate
from roles.follower import Follower
from roles.leader import Leader
from roles.role import Role


class Node:
    def __init__(
        self,
        server: str,
        port: int = 9092,
        node_id: UUID | None = None,
        peers: list[str] | None = None,
        role: Role = Role.FOLLOWER,
        log: RaftLog | None = None,
    ) -> None:
        self.node_id: UUID = node_id or uuid4()
        self.peers: list[str] = peers or []
        self.__server = server
        self.__port = port
        self.__role: Role = role
        self.__log: RaftLog = log or RaftLog(self.node_id)

    async def run(self) -> None:
        while True:
            await self.__run_next_role()

    async def __run_next_role(self) -> None:
        match self.__role:
            case Role.FOLLOWER:
                async with Follower(
                    server=self.__server, port=self.__port, node_id=self.node_id
                ) as follower:
                    self.__role = await follower.run()

            case Role.CANDIDATE:
                # candidate = Candidate(self.__message_service, self.peers, self.__log)
                # self.__role = await candidate.elect()
                self.__role = Role.LEADER

            case Role.LEADER:
                async with Leader(
                    log=self.__log, server=self.__server, port=self.__port
                ) as leader:
                    self.__role = await leader.run()

                raise NotImplementedError("Last role")
