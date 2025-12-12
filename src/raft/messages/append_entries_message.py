from dataclasses import dataclass


@dataclass
class AppendEntriesMessage:
    term: int
    sender: str
    entries: list[dict]
    previous_log_index: int
    previous_log_term: int
    commit_index: int
