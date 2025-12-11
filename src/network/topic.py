from enum import StrEnum, auto


class Topic(StrEnum):
    ASSIGN = auto()
    APPEND_ENTRIES = auto()
    APPEND_ENTRIES_RESPONSE = auto()
    VOTE = auto()
    VOTE_REQUEST = auto()
    OUTPUT = auto()
    INPUT = auto()
    REPORT = auto()
    PING = auto()
    PING_RESPONSE = auto()
