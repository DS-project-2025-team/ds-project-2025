from collections import deque
from collections.abc import Iterable

from entities.sat_formula import SatFormula


class LeaderState:
    def __init__(
        self,
        nodes: dict[str, dict] | None = None,
        completed_tasks: list[bool] | None = None,
        formulas: Iterable[SatFormula] | None = None,
    ) -> None:
        self.nodes: dict[str, dict] = nodes or {}
        self.completed_tasks: list[bool] = completed_tasks or []
        self.formulas: deque[SatFormula] = deque(formulas or [])

    def mark_done(self, task: int) -> None:
        if task >= len(self.completed_tasks):
            return

        self.completed_tasks[task] = True

    def __repr__(self) -> str:
        return (
            f"LeaderState(nodes={self.nodes}, "
            f"completed_tasks={self.completed_tasks}, "
            f"formulas={list(self.formulas)})"
        )
