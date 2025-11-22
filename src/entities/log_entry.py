class LogEntry:
    def __init__(self, term: int, command: dict) -> None:
        self.term = term  # Raft term number
        self.command = command  # Command to be applied to the state machine
