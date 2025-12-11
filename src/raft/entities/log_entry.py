from collections.abc import Callable

from raft.entities.leader_state import LeaderState


class LogEntry:
    def __init__(self, leader_state: LeaderState, term: int, index: int) -> None:
        self.__leader_state = leader_state
        self.__term = term
        self.__index = index
        self.__operation: Callable[[LeaderState], LeaderState] = (
            lambda _: self.__leader_state
        )

    def operate(self, state: LeaderState) -> None:
        self.__operation(state)

    @property
    def term(self) -> int:
        return self.__term

    @property
    def index(self) -> int:
        return self.__index

    @index.setter
    def index(self, index: int) -> None:
        self.__index = index

    def to_dict(self) -> dict[str, object]:
        return {
            "term": self.__term,
            "index": self.__index,
            "state": self.__leader_state.to_dict(),
        }
