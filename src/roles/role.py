from enum import Enum, auto


class Role(Enum):
    LEADER = auto()
    FOLLOWER = auto()
    CANDIDATE = auto()
