from raft.entities.leader_state import LeaderState
from raft.entities.log_entry import LogEntry
from raft.raft_log import RaftLog
from entities.sat_formula import SatFormula


class LogEntryFactory:
    @staticmethod
    def complete_task(raftlog: RaftLog, task: int) -> LogEntry:
        return LogEntry(raftlog, lambda state: state.mark_done(task))

    @staticmethod
    def add_formula(raftlog: RaftLog, formula: SatFormula) -> LogEntry:
        return LogEntry(raftlog, lambda state: state.formulas.append(formula))

    @staticmethod
    def pop_formula(raftlog: RaftLog) -> LogEntry:
        def update_state(state: LeaderState) -> None:
            if state.formulas:
                state.formulas.popleft()

            state.completed_tasks = []

        return LogEntry(raftlog, update_state)

    @staticmethod
    def set_completed_tasks(raftlog: RaftLog, completed_tasks: list[bool]) -> LogEntry:
        def update_state(state: LeaderState) -> None:
            state.completed_tasks = completed_tasks

        return LogEntry(raftlog, update_state)
