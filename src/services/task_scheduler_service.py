from collections import deque
from collections.abc import Iterable, Sequence

from entities.sat_formula import SatFormula


class TaskSchedulerService:
    def __init__(
        self,
        formula: SatFormula,
        tasks: Iterable[int] | None = None,
        completed_tasks: Sequence[int] | None = None,
        tasks_remaining: int = 0,
    ) -> None:
        self.__formula: SatFormula = formula
        self.__tasks: deque[int] = deque(tasks or [])
        self.__completed_tasks: list[int] = list(completed_tasks or [])
        self.__tasks_remaining: int = tasks_remaining

    def next_task(self) -> int | None:
        task = None

        while self.__tasks:
            task = self.__tasks.popleft()

            if not self.__completed_tasks[task]:
                self.__tasks.append(task)
                break

        return task
