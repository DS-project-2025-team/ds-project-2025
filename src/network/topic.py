from enum import StrEnum, auto


class Topic(StrEnum):
    ASSIGN = auto()
    APPENDENTRY = auto()
    APPENDENTRY_RESPONSE = auto()
    VOTE = auto()
    VOTE_REQUEST = auto()
    OUTPUT = auto()
    INPUT = auto()
    REPORT = auto()
