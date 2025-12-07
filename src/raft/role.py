from enum import StrEnum, auto


class Role(StrEnum):
    LEADER = auto()
    FOLLOWER = auto()
    CANDIDATE = auto()
