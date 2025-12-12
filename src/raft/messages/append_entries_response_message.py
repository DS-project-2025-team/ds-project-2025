from dataclasses import dataclass
from uuid import UUID


@dataclass
class AppendEntriesResponseMessage:
    term: int
    follower_id: UUID
    previous_log_index: int
    success: bool
