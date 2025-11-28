from collections.abc import Callable

from entities.leader_state import LeaderState


class LogEntry:
    def __init__(self, term: int, operation: Callable[[LeaderState], None]) -> None:
        self.__term = term
        self.__operation: Callable[[LeaderState], None] = operation

    def operate(self, state: LeaderState) -> None:
        self.__operation(state)
