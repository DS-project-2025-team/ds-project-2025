from collections.abc import Callable

from entities.leader_state import LeaderState


class LogEntry:
    def __init__(
        self, term: int, operation: Callable[[LeaderState], LeaderState]
    ) -> None:
        self.__term = term
        self.__operation: Callable[[LeaderState], LeaderState] = operation

    def operate(self, state: LeaderState) -> LeaderState:
        return self.__operation(state)
