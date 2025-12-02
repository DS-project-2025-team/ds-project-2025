from entities.log_entry import LogEntry


class LogEntryFactory:
    @staticmethod
    def complete_task(term: int, task: int) -> LogEntry:
        return LogEntry(term, lambda state: state.mark_done(task))
