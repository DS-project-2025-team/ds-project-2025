import asyncio
from collections.abc import Iterable
from uuid import UUID

from entities.sat_formula import SatFormula
from raft.entities.leader_state import LeaderState
from raft.entities.log_entry import LogEntry
from services.logger_service import logger


class Log:
    def __init__(
        self,
        entries: Iterable[LogEntry] | None = None,
        commit_index: int = -1,
        term: int = 0,
        voted_for: UUID | None = None,
        leader_state: LeaderState | None = None,
    ) -> None:
        self.__term: int = term
        self.__voted_for: UUID | None = voted_for

        self.entries: list[LogEntry] = list(entries or [])

        self.commit_index: int = commit_index
        self.lock = asyncio.Lock()
        self.append_lock: asyncio.Lock = asyncio.Lock()
        self.last_acked_index = -1
        self.leader_state: LeaderState = leader_state or LeaderState()

    @property
    def term(self) -> int:
        return self.__term

    @term.setter
    def term(self, new_term: int) -> None:
        if new_term < self.__term:
            logger.warning(
                f"Attempted to set term {self.term} to smaller term {new_term}"
            )
            return

        self.__term = new_term
        self.__voted_for = None

    @property
    def voted_for(self) -> UUID | None:
        return self.__voted_for

    @voted_for.setter
    def voted_for(self, node_id: UUID) -> None:
        self.__voted_for = node_id

    @property
    def completed_tasks(self) -> list[bool]:
        return self.leader_state.completed_tasks

    @property
    def current_formula(self) -> SatFormula | None:
        if not self.leader_state.formulas:
            return None

        return self.leader_state.formulas[0]

    @property
    def last_log_index(self) -> int:
        """
        Return index of the last log entry if exists, otherwise -1.
        """

        if not self.entries:
            return -1

        return self.entries[-1].index

    @property
    def last_log_term(self) -> int:
        """
        Return term of the last log entry if exists, otherwise 0.
        """

        if not self.entries:
            return 0

        return self.entries[-1].term

    def append(self, entry: LogEntry) -> None:
        entry.index = self.entries.__len__()
        self.entries.append(entry)
        logger.debug(f"Applied entry {entry.to_dict()} to raftlog")

    def commit(self) -> None:
        if self.commit_index >= len(self.entries):
            logger.debug(
                f"No new entries to commit, commit_index: {self.commit_index}"
                f"entries length: {len(self.entries)}"
            )
            return

        entry = self.entries[self.commit_index]

        logger.info(
            "Committing log entry index: %s, state before: %s",
            entry.index,
            self.leader_state,
        )

        self.leader_state = entry.operate(self.leader_state)
        self.commit_index += 1

        logger.info(
            "Committed log entry index: %s, state after: %s",
            entry.index,
            self.leader_state,
        )

    def revert(self, index: int) -> None:
        if index < -1 or index >= len(self.entries):
            raise IndexError("Index out of range")

        # Trim entries to the requested index and update commit_index
        self.entries = self.entries[: index + 1]
        self.commit_index = index

    def get_commit_index(self) -> int:
        return self.commit_index

    def get_raftlog_entries(self, fromindex: int = 0) -> Iterable[LogEntry]:
        return self.entries[fromindex:]

    def get_entry_at_index(self, index: int) -> LogEntry:
        return self.entries[index]
