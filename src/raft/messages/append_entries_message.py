from dataclasses import dataclass
from uuid import UUID

from raft.entities.log_entry import LogEntry


@dataclass
class AppendEntriesMessage:
    term: int
    leader_id: UUID
    entries: list[LogEntry]
    previous_log_index: int
    previous_log_term: int
    leader_commit: int
