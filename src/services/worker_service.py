import asyncio
from concurrent.futures import ProcessPoolExecutor
from contextlib import AbstractContextManager
from types import TracebackType
from typing import Self

from entities.sat_formula import SatFormula
from utils.check_sat import check_sat_formula
from utils.task import get_subinterval


def compute(formula: SatFormula, task: int, exponent: int) -> bool:
    begin, end = get_subinterval(2**exponent, task)
    return check_sat_formula(formula, begin, end)


class WorkerService(AbstractContextManager):
    def __init__(self, executor: ProcessPoolExecutor | None = None) -> None:
        self.__executor: ProcessPoolExecutor = executor or ProcessPoolExecutor()

    def __enter__(self) -> Self:
        self.__executor.__enter__()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.__executor.__exit__(exc_type, exc_value, traceback)

    async def run_task(
        self,
        formula: SatFormula,
        task: int,
        exponent: int,
    ) -> bool:
        return await asyncio.get_event_loop().run_in_executor(
            self.__executor, compute, formula, task, exponent
        )
