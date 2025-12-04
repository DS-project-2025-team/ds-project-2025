from entities.leader_state import LeaderState
from entities.log_entry import LogEntry
from entities.sat_formula import SatFormula


class LogEntryFactory:
    @staticmethod
    def complete_task(term: int, task: int) -> LogEntry:
        return LogEntry(term, lambda state: state.mark_done(task))

    @staticmethod
    def add_formula(term: int, formula: SatFormula) -> LogEntry:
        return LogEntry(term, lambda state: state.formulas.append(formula))

    @staticmethod
    def pop_formula(term: int) -> LogEntry:
        def update_state(state: LeaderState) -> None:
            if state.formulas:
                state.formulas.popleft()

            state.completed_tasks = []

        return LogEntry(term, update_state)

    @staticmethod
    def set_completed_tasks(term: int, completed_tasks: list[bool]) -> LogEntry:
        def update_state(state: LeaderState) -> None:
            state.completed_tasks = completed_tasks

        return LogEntry(term, update_state)
