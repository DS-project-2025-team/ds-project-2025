import asyncio
from collections.abc import Callable, Coroutine
from contextlib import AbstractContextManager
from multiprocessing.pool import Pool
from types import TracebackType
from typing import Self

from entities.sat_formula import SatFormula
from utils.check_sat import check_sat_formula
from utils.task import get_subinterval


class WorkerService(AbstractContextManager):
    def __init__(self, processes: int = 8) -> None:
        self.__pool: Pool = Pool(processes)

    def __enter__(self) -> Self:
        self.__pool.__enter__()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.__pool.__exit__(exc_type, exc_value, traceback)

    def run_task(
        self,
        formula: SatFormula,
        task: int,
        exponent: int,
        callback: Callable[[bool], Coroutine],
    ) -> None:
        self.__pool.apply_async(
            self.__compute,
            (formula, task, exponent),
            callback=lambda result: asyncio.run(callback(result)),
        )

    def __compute(self, formula: SatFormula, task: int, exponent: int) -> bool:
        begin, end = get_subinterval(2**exponent, task)
        return check_sat_formula(formula, begin, end)
