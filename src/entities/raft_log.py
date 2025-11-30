from uuid import UUID

from entities.leader_state import LeaderState
from entities.log_entry import LogEntry


class RaftLog:
    def __init__(self, node_id: UUID) -> None:
        self.node_id: UUID = node_id
        self.entries: list[LogEntry] = []

        self.commit_index: int = -1
        self.term: int = 0
        self.leader_id: str | None = None

        self.leader_state: LeaderState = LeaderState()

    @property
    def completed_tasks(self) -> list[int]:
        return self.leader_state.completed_tasks

    def append(self, entry: LogEntry) -> None:
        self.entries.append(entry)

    def commit(self) -> None:
        if self.commit_index + 1 >= len(self.entries):
            return

        entry = self.entries[self.commit_index]

        entry.operate(self.leader_state)
        self.commit_index += 1

    def revert(self, index: int) -> None:
        if index < -1 or index >= len(self.entries):
            raise IndexError("Index out of range")

        # Trim entries to the requested index and update commit_index
        self.entries = self.entries[: index + 1]
        self.commit_index = index
