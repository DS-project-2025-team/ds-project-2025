from collections import deque
from collections.abc import Iterable

from entities.sat_formula import SatFormula


class LeaderState:
    def __init__(
        self,
        completed_tasks: Iterable[bool] | None = None,
        formulas: Iterable[SatFormula] | None = None,
    ) -> None:
        self.completed_tasks: list[bool] = list(completed_tasks or [])
        self.formulas: deque[SatFormula] = deque(formulas or [])

    def mark_done(self, task: int) -> None:
        if task >= len(self.completed_tasks):
            return

        self.completed_tasks[task] = True

    def __repr__(self) -> str:
        return (
            f"completed_tasks={self.completed_tasks}, formulas={list(self.formulas)})"
        )
