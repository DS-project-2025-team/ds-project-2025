from collections.abc import Iterable
from uuid import UUID, uuid4

from entities.leader_state import LeaderState
from entities.log_entry import LogEntry
from entities.sat_formula import SatFormula
from services.logger_service import logger


class RaftLog:
    def __init__(
        self,
        entries: Iterable[LogEntry] | None = None,
        commit_index: int = 0,
        term: int = 0,
        leader_id: UUID | None = None,
        leader_state: LeaderState | None = None,
    ) -> None:
        self.entries: list[LogEntry] = list(entries or [])

        self.commit_index: int = commit_index
        self.term: int = term
        self.leader_id: UUID = leader_id or uuid4()

        self.leader_state: LeaderState = leader_state or LeaderState()

    @property
    def completed_tasks(self) -> list[bool]:
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

        logger.info(f"Committing log entry, state before: {self.leader_state}")

        entry.operate(self.leader_state)
        self.commit_index += 1

        logger.info(f"Committed log entry, state after: {self.leader_state}")

    def revert(self, index: int) -> None:
        if index < -1 or index >= len(self.entries):
            raise IndexError("Index out of range")

        # Trim entries to the requested index and update commit_index
        self.entries = self.entries[: index + 1]
        self.commit_index = index
