from entities.sat_formula import SatFormula
from raft.entities.leader_state import LeaderState
from raft.entities.log import Log
from raft.entities.log_entry import LogEntry


class LogEntryFactory:
    @staticmethod
    def complete_task(raftlog: Log, task: int) -> LogEntry:
        return LogEntry(raftlog, lambda state: state.mark_done(task))

    @staticmethod
    def add_formula(raftlog: Log, formula: SatFormula) -> LogEntry:
        return LogEntry(raftlog, lambda state: state.formulas.append(formula))

    @staticmethod
    def pop_formula(raftlog: Log) -> LogEntry:
        def update_state(state: LeaderState) -> None:
            if state.formulas:
                state.formulas.popleft()

            state.completed_tasks = []

        return LogEntry(raftlog, update_state)

    @staticmethod
    def set_completed_tasks(raftlog: Log, completed_tasks: list[bool]) -> LogEntry:
        def update_state(state: LeaderState) -> None:
            state.completed_tasks = completed_tasks

        return LogEntry(raftlog, update_state)
