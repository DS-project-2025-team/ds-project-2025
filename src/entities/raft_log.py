from typing import Any

from entities.leader_state import LeaderState
from entities.log_entry import LogEntry


class RaftLog:
    def __init__(self, node_id: str) -> None:
        self.node_id = node_id

        # List of LogEntry
        self.entries: list[LogEntry] = []

        # Raft state
        self.commit_index: int = -1
        self.term: int = 0
        self.leader_id: str | None = None

        self.leader_state: LeaderState = LeaderState()  # cluster members

    def commit(self) -> None:
        if self.commit_index + 1 >= len(self.entries):
            return

        self.commit_index += 1
        entry = self.entries[self.commit_index]
        self.leader_state = entry.operate(self.leader_state)

    def revert(self, index: int) -> None:
        # Validate index bounds (allow reverting back to earlier entries)
        if index < -1 or index >= len(self.entries):
            raise IndexError("Index out of range")

        # Trim entries to the requested index and update commit_index
        self.entries = self.entries[: index + 1]
        self.commit_index = index

    def apply_entry(self, command: dict[str, Any]) -> None:
        match command["type"]:
            case "NODE_JOIN":
                node_id = command["node_id"]
                self.leader_state.nodes[node_id] = {"status": "alive"}

            case "ASSIGN_TASK":
                task_id = command["task_id"]
                node_id = command["node_id"]
                self.leader_state.tasks[task_id] = node_id
                self.leader_state.uncompleted_tasks.add(task_id)

            case "REPORT_RESULT":
                pass
