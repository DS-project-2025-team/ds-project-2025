from collections.abc import Iterable
from uuid import UUID, uuid4

from entities.leader_state import LeaderState
from entities.log_entry import LogEntry
from entities.sat_formula import SatFormula


class RaftLog:
    def __init__(
        self,
        entries: Iterable[LogEntry],
        commit_index: int = -1,
        term: int = 0,
        leader_id: UUID | None = None,
        leader_state: LeaderState | None = None,
    ) -> None:
        self.entries: list[LogEntry] = list(entries) or []

        self.commit_index: int = commit_index
        self.term: int = term
        self.leader_id: UUID = leader_id or uuid4()

        self.leader_state: LeaderState = leader_state or LeaderState()

    @property
    def completed_tasks(self) -> list[int]:
        return self.leader_state.completed_tasks

    @property
    def current_formula(self) -> SatFormula | None:
        if not self.leader_state.formulas:
            return None

        return self.leader_state.formulas[0]

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
