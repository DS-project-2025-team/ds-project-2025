from collections import deque
from collections.abc import Iterable, Sequence

from entities.sat_formula import SatFormula
from utils.task import get_tasks_from_formula


class TaskSchedulerService:
    def __init__(
        self,
        formula: SatFormula,
        exponent: int,
        tasks: Iterable[int] | None = None,
        completed_tasks: Sequence[bool] | None = None,
    ) -> None:
        self.__tasks: deque[int] = deque(
            tasks or get_tasks_from_formula(formula, exponent)
        )
        self.__completed_tasks: list[bool] = list(
            completed_tasks or [False] * len(self.__tasks)
        )
        self.__tasks_remaining: int = len(self.__tasks)

    def next_task(self) -> int | None:
        task = None

        while self.__tasks:
            task = self.__tasks.popleft()

            if not self.__completed_tasks[task]:
                self.__tasks.append(task)
                break

        return task

    def complete_task(self, task: int, result: bool) -> bool:
        if not self.__completed_tasks[task]:
            self.__tasks_remaining -= 1

        self.__completed_tasks[task] = True

        return result or self.__tasks_remaining == 0
