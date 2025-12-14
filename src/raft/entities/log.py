import asyncio
from collections.abc import Iterable
from uuid import UUID

from entities.sat_formula import SatFormula
from entities.server_address import ServerAddress
from raft.entities.leader_state import LeaderState
from raft.entities.log_entry import LogEntry
from raft.entities.partial_log_entry import PartialLogEntry
from services.logger_service import logger


class Log:
    def __init__(
        self,
        entries: Iterable[LogEntry] | None = None,
        commit_index: int = -1,
        term: int = 0,
        voted_for: UUID | None = None,
        nodes: list[dict[str, object]] | None = None,
        leader_state: LeaderState | None = None,
    ) -> None:
        self.__term: int = term
        self.__voted_for: UUID | None = voted_for
        self.nodes: list[dict[str, object]] = nodes or []
        self.entries: list[LogEntry] = list(entries or [])
        self.commit_event = asyncio.Event()
        self.__commit_index: int = commit_index
        self.lock = asyncio.Lock()
        self.append_lock: asyncio.Lock = asyncio.Lock()
        self.leader_state: LeaderState = leader_state or LeaderState()

    @property
    def commit_index(self) -> int:
        return self.__commit_index

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
        logger.debug("last_log_index : log entries: %s", len(self.entries))

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

    def append(self, raw_entry: PartialLogEntry) -> int:
        index = self.last_log_index + 1

        entry: LogEntry = LogEntry.from_partial(
            raw_entry,
            index,
        )

        self.entries.append(entry)
        logger.debug(f"Appended entry index: {index} {entry.to_dict()} to raftlog")

        return index

    def commit(self, commit_index: int) -> None:
        """
        Commit all entries before given index (inclusive).

        Args:
            commit_index (int): New commit index.
        """

        if commit_index >= len(self.entries):
            logger.debug(
                f"No new entries to commit, commit_index: {commit_index} "
                f"entries length: {len(self.entries)}"
            )
            return

        logger.info(
            "Committing log entry index: %s, state before: %s",
            commit_index,
            self.leader_state,
        )
        entry = self.entries[commit_index]

        self.leader_state = entry.operate(self.leader_state)
        self.__commit_index = commit_index

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
        self.__commit_index = index

    def get_commit_index(self) -> int:
        return self.commit_index

    def get_raftlog_entries(self, fromindex: int = 0) -> Iterable[LogEntry]:
        return self.entries[fromindex:]

    def get_entry_at_index(self, index: int) -> LogEntry:
        return self.entries[index]

    def get_uncommitted_entries(self) -> Iterable[LogEntry]:
        return self.entries[self.commit_index + 1 :]

    """
    Copy tuples from nodelist to log.nodes list with
    initial value -1 for last_acked_index
    """
    def set_nodes(self, nodelist: list) -> None:
        if not self.nodes:
            self.nodes = [
                {"uuid": uuid, "server": server, "last_index": -1} 
                for (uuid, server) in nodelist
            ]

    def get_nodes(self) -> list:
        return list(self.nodes)
