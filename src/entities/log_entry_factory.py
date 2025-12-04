from entities.log_entry import LogEntry
from entities.sat_formula import SatFormula


class LogEntryFactory:
    @staticmethod
    def complete_task(term: int, task: int) -> LogEntry:
        return LogEntry(term, lambda state: state.mark_done(task))

    @staticmethod
    def add_formula(term: int, formula: SatFormula) -> LogEntry:
        return LogEntry(term, lambda state: state.formulas.append(formula))
