from dataclasses import dataclass

from raft.entities.leader_state import LeaderState


@dataclass
class PartialLogEntry:
    """
    Intermediate type for non-appended entry.
    """

    leader_state: LeaderState
    term: int
