from __future__ import annotations

from collections.abc import Callable

from raft.entities.leader_state import LeaderState


class LogEntry:
    def __init__(
        self, raftlog: "RaftLog", operation: Callable[[LeaderState], None]
    ) -> None:
        term = raftlog.term
        self.__raftlog = raftlog
        self.__term = term
        self.__index = 0
        self.__operation: Callable[[LeaderState], None] = operation

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
        raftlog = self.__raftlog
        prev_index = self.__index - 1
        prev_log_entry = raftlog.get_entry_at_index(prev_index)
        commit_index = raftlog.get_commit_index()
        return {
            "term": self.__term,
            "index": self.__index,
            "prev_log_index": prev_index,
            "prev_log_term": prev_log_entry.__term,
            "commit_index": commit_index,
        }
