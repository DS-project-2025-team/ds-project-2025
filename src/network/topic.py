from enum import StrEnum, auto


class Topic(StrEnum):
    ASSIGN = auto()
    HEARTBEAT = auto()
    VOTE = auto()
    VOTE_REQUEST = auto()
    OUTPUT = auto()
    INPUT = auto()
