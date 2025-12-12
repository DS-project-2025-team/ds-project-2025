from dataclasses import dataclass
from uuid import UUID


@dataclass
class AppendEntriesMessage:
    term: int
    leader_id: UUID
    entries: list[dict]
    previous_log_index: int
    previous_log_term: int
    commit_index: int
