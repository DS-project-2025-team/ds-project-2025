from contextlib import AbstractAsyncContextManager
from multiprocessing.pool import Pool
from types import TracebackType
from typing import Self


class WorkerService(AbstractAsyncContextManager):
    def __init__(self, processes: int = 8) -> None:
        self.__pool: Pool = Pool(processes)

    async def __aenter__(self) -> Self:
        self.__pool.__enter__()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.__pool.__exit__(exc_type, exc_value, traceback)
