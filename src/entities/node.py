from roles.candidate import Candidate
from roles.follower import Follower
from roles.leader import Leader
from roles.role import Role
from services.message_service import (
    MessageService,
)


class Node:
    def __init__(
        self,
        message_service: MessageService,
        role: Role = Role.FOLLOWER,
    ) -> None:
        self.__role: Role = role
        self.__message_service: MessageService = message_service

    def run(self) -> None:
        while True:
            self.__run_next_role()

    def __run_next_role(self) -> None:
        match self.__role:
            case Role.FOLLOWER:
                follower = Follower()
                self.__role = follower.run()

            case Role.CANDIDATE:
                self.__role = Candidate.elect()

            case Role.LEADER:
                leader = Leader(self.__message_service)
                self.__role = leader.run()

                raise NotImplementedError("Last role")
