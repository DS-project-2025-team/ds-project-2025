from entities.raft_log import RaftLog
from network.message_service import (
    MessageService,
)
from roles.candidate import Candidate
from roles.follower import Follower
from roles.leader import Leader
from roles.role import Role


class Node:
    def __init__(
        self,
        message_service: MessageService,
        role: Role = Role.FOLLOWER,
        log: RaftLog | None = None,
    ) -> None:
        self.__role: Role = role
        self.__message_service: MessageService = message_service
        self.__log: RaftLog = log or RaftLog("1")

    def run(self) -> None:
        while True:
            self.__run_next_role()

    def __run_next_role(self) -> None:
        match self.__role:
            case Role.FOLLOWER:
                follower = Follower(self.__message_service)
                self.__role = follower.run()

            case Role.CANDIDATE:
                self.__role = Candidate.elect()

            case Role.LEADER:
                leader = Leader(self.__message_service, self.__log)
                self.__role = leader.run()

                raise NotImplementedError("Last role")
