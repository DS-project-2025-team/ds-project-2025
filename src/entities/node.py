from roles.candidate import Candidate
from roles.follower import Follower
from roles.leader import Leader
from roles.role import Role
from services.message_service import (
    MessageService,
)
from services.message_service import (
    message_service as default_message_service,
)


class Node:
    def __init__(
        self,
        role: Role = Role.FOLLOWER,
        message_service: MessageService = default_message_service,
    ) -> None:
        self.__role: Role = role
        self.__message_service: MessageService = message_service

    def run(self) -> None:
        while True:
            self.__run_next_role()

    def __run_next_role(self) -> None:
        match self.__role:
            case Role.FOLLOWER:
                follower = Follower(election_timeout=None)
                self.__role = follower.run()

            case Role.CANDIDATE:
                self.__role = Candidate.elect()

            case Role.LEADER:
                leader = Leader()
                self.__role = leader.run()

                raise NotImplementedError("Last role")
