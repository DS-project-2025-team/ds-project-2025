from operator import concat

from entities.sat_formula import SatFormula
from raft.entities.leader_state import LeaderState
from raft.entities.partial_log_entry import PartialLogEntry


class LogEntryFactory:
    @staticmethod
    def complete_task(task: int, state: LeaderState, term: int) -> PartialLogEntry:
        formulas = state.formulas.copy()
        completed_tasks = (
            (i == task) or x for i, x in enumerate(state.completed_tasks)
        )

        return PartialLogEntry(LeaderState([], completed_tasks, formulas), term)

    @staticmethod
    def add_formula(
        formula: SatFormula, state: LeaderState, term: int
    ) -> PartialLogEntry:
        formulas = concat(list(state.formulas), [formula])
        completed_tasks = state.completed_tasks.copy()

        return PartialLogEntry(LeaderState([], completed_tasks, formulas), term)

    @staticmethod
    def pop_formula(state: LeaderState, term: int) -> PartialLogEntry:
        formulas = []

        if state.formulas:
            formulas = list(state.formulas)[1:]

        return PartialLogEntry(LeaderState([], [], formulas), term)

    @staticmethod
    def set_completed_tasks(
        completed_tasks: list[bool], state: LeaderState, term: int
    ) -> PartialLogEntry:
        formulas = state.formulas.copy()

        return PartialLogEntry(LeaderState([], completed_tasks, formulas), term)
