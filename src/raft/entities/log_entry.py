from typing import Any

from raft.entities.leader_state import LeaderState
from raft.entities.partial_log_entry import PartialLogEntry


class LogEntry:
    def __init__(self, leader_state: LeaderState, term: int, index: int) -> None:
        self.__leader_state = leader_state
        self.__term = term
        self.__index = index

    def operate(self, _: LeaderState) -> LeaderState:
        """
        Compute new leader state based on current state. Not yet implemented.

        Args:
            _ (LeaderState): Current leader state.

        Returns:
            LeaderState: New leader state.
        """

        return self.__leader_state

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

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "LogEntry":
        leader_state = LeaderState.from_dict(data["state"])  # type: ignore
        term = data["term"]  # type: ignore
        index = data["index"]  # type: ignore

        return LogEntry(leader_state, term, index)

    @staticmethod
    def from_partial(partial: PartialLogEntry, index: int) -> "LogEntry":
        return LogEntry(partial.leader_state, partial.term, index)

    def get_index(self) -> int:
        return self.__index
