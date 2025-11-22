from typing import Any

from .log_entry import LogEntry


class RaftLog:
    def __init__(self, node_id: str) -> None:
        self.node_id = node_id

        # List of LogEntry
        self.entries: list[LogEntry] = []

        # Raft state
        self.commit_index: int = -1
        self.term: int = 0
        self.leader_id: str | None = None

        # Shared system state
        self.nodes: dict[str, dict] = {}  # cluster members
        self.tasks: dict[str, str] = {}  # {task_id: node_id}
        self.uncompleted_tasks: set[str] = set()  # task_ids not yet completed
        self.formula: str | None = None  # 3-SAT formula

    def commit(self) -> None:
        # apply next uncommitted entry
        if self.commit_index + 1 < len(self.entries):
            self.commit_index += 1
            entry = self.entries[self.commit_index]
            self.apply_entry(entry.command)

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
                self.nodes[node_id] = {"status": "alive"}

            case "NODE_FAILS":
                node_id = command["node_id"]
                if node_id in self.nodes:
                    self.nodes[node_id]["status"] = "failed"
                for task_id, assigned_node in list(self.tasks.items()):
                    if assigned_node == node_id:
                        del self.tasks[task_id]
                        self.uncompleted_tasks.add(task_id)

            case "ASSIGN_TASK":
                task_id = command["task_id"]
                node_id = command["node_id"]
                self.tasks[task_id] = node_id
                self.uncompleted_tasks.add(task_id)

            case "REPORT_RESULT":
                pass
