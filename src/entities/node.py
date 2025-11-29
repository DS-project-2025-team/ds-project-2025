import uuid
from entities.raft_log import RaftLog
from network.message_service import (
    MessageService,
)
from roles.candidate import Candidate
from roles.follower import Follower
from roles.leader import Leader
from roles.role import Role
from network.message_service import MessageService


class Node:
    def __init__(
        self,
        message_service: MessageService,
        node_id: str | None = None,
        peers: list[str] | None = None,
        role: Role = Role.FOLLOWER,
        log: RaftLog | None = None,
    ) -> None:
        self.node_id: str = node_id or str(uuid.uuid4())
        self.peers: list[str] = peers or []
        self.__role: Role = role
        self.__message_service: MessageService = message_service
        self.__log: RaftLog = log or RaftLog(self.node_id)

    async def run(self) -> None:
        while True:
            await self.__run_next_role()

    async def __run_next_role(self) -> None:
        match self.__role:
            case Role.FOLLOWER:
                follower = Follower(self.node_id, self.__message_service)
                self.__role = await follower.run()

            case Role.CANDIDATE:
                candidate = Candidate(self.__message_service, self.peers, self.__log)
                self.__role = await Candidate.elect()

            case Role.LEADER:
                leader = Leader(self.node_id, self.__message_service, self.__log)
                self.__role = await leader.run()

                raise NotImplementedError("Last role")
