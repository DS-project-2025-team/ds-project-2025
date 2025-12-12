import asyncio
import random
from contextlib import AbstractAsyncContextManager
from types import TracebackType
from typing import Literal, Self

from entities.sat_formula import SatFormula
from entities.second import Second
from raft.entities.log import Log
from raft.network.follower_messager import FollowerMessager
from raft.roles.role import Role
from services.logger_service import logger
from services.worker_service import WorkerService
from utils.async_loop import async_loop


class Follower(AbstractAsyncContextManager):
    def __init__(
        self,
        log: Log,
        messager: FollowerMessager,
        election_timeout: Second | None = None,
        worker: WorkerService | None = None,
    ) -> None:
        self.__messager: FollowerMessager = messager
        self.__worker: WorkerService = worker or WorkerService()
        self.__log: Log = log

        self.__election_timeout: Second = election_timeout or Second(
            5 + random.randint(0, 10)
        )

    async def __aenter__(self) -> Self:
        self.__worker.__enter__()

        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.__worker.__exit__(exc_type, exc_value, traceback)

    async def run(self) -> Literal[Role.CANDIDATE]:
        try:
            async with asyncio.TaskGroup() as group:
                group.create_task(self.__handle_append_entries())
                group.create_task(self.__handle_assign())

                logger.info("Follower is running")
        except* TimeoutError:
            logger.warning("Missing heartbeat, election timeout elapsed.")

        logger.info("Changing role to CANDIDATE")
        return Role.CANDIDATE

    @async_loop
    async def __handle_append_entries(self) -> None:
        message = await self.__messager.receive_append_entries(self.__election_timeout)

        logger.debug(f"Received AppendEntriesMessage: {message}")
        await self.__messager.send_append_entries_response(self.__log.term)

    @async_loop
    async def __handle_assign(self) -> None:
        formula, task, exponent = await self.__messager.receive_assign()
        logger.info(
            f"Received work: formula {formula}, task {task}, exponent {exponent}"
        )

        result = await self.__worker.run_task(formula, task, exponent)

        await self.__send_result(formula, task, result)

    async def __send_result(self, formula: SatFormula, task: int, result: bool) -> None:
        await self.__messager.send_report(formula, task, result)

        logger.info(f"Sent result for task {task}: {result}")
