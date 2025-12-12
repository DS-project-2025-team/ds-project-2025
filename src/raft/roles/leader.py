import asyncio
from contextlib import suppress
from typing import Literal
from uuid import UUID

from config import SUBINTERVAL_EXPONENT
from entities.sat_formula import SatFormula
from entities.second import Second
from entities.task_queue import TaskQueue
from raft.entities.log import Log
from raft.entities.log_entry import LogEntry
from raft.entities.log_entry_factory import LogEntryFactory
from raft.network.leader_messager import LeaderMessager
from raft.roles.role import Role
from services.logger_service import logger
from utils.async_loop import async_loop
from utils.hash_sat_formula import hash_sat_formula


class Leader:
    def __init__(
        self,
        log: Log,
        messager: LeaderMessager,
        task_queue: TaskQueue | None = None,
        follower_commit_indexes: dict[UUID, int] | None = None,
    ) -> None:
        self.__messager: LeaderMessager = messager

        self.__task_queue: TaskQueue | None = task_queue
        self.__log: Log = log
        self.__follower_commit_indexes: dict[UUID, int] = {}

    async def run(self) -> Literal[Role.FOLLOWER]:
        try:
            async with asyncio.TaskGroup() as group:
                _task1 = group.create_task(self.__send_append_entries())
                _task2 = group.create_task(self.__receive_append_entries_response())
                _task3 = group.create_task(self.__handle_input(Second(1)))
                _task4 = group.create_task(self.__assign_task())
                _task5 = group.create_task(self.__handle_report())

                logger.info("Leader is running")
        except Exception as error:
            raise NotImplementedError(
                "Leader failure handling not implemented"
            ) from error

        logger.info("Changing role to FOLLOWER")
        return Role.FOLLOWER

    async def __receive_input(self, timeout: Second) -> SatFormula:
        return await self.__messager.receive_input(timeout)

    async def __send_output(self, result: bool) -> None:
        logger.info(f"Computed result: {result}")

        await self.__messager.send_output(result, hash(self.__task_queue))

        logger.info(f"Sent result {result}")

    @async_loop
    async def __send_append_entries(self) -> None:
        entries = self.__log.get_uncommitted_entries()

        await self.__messager.send_append_entries(
            entries=entries,
            previous_log_index=self.__log.commit_index,
            previous_log_term=self.__log.term,
            commit_index=self.__log.commit_index,
        )

        await asyncio.sleep(2)

    async def __append_entry(self, entry: LogEntry) -> None:
        async with self.__log.append_lock:
            logger.debug(f"Appending entry {entry.to_dict()} to log")
            self.__log.append(entry)
            self.__log.commit()

    @async_loop
    async def __receive_append_entries_response(self) -> None:
        """
        Read messages via append_entries_response_consumer
        """

        await self.__messager.receive_append_entries_response()

    async def __send_task(self, formula: SatFormula, task: int, exponent: int) -> None:
        await self.__messager.send_task(formula, task, exponent)

        logger.info(f"Assigned task {task} of formula {hash_sat_formula(formula)}")

    @async_loop
    async def __handle_report(self) -> None:
        result = await self.__messager.receive_report(hash(self.__task_queue))

        if result is None:
            return

        task, satisfiable = result

        await self.__complete_task(task)

        if not (self.__task_queue and self.__task_queue.is_done(satisfiable)):
            return

        await self.__send_output(satisfiable)
        await self.__reset_task_queue()

    @async_loop
    async def __handle_input(self, timeout: Second) -> None:
        with suppress(TimeoutError):
            formula = await self.__receive_input(timeout)

            logger.info(f"Received new SAT formula: {formula}")

            entry = LogEntryFactory.add_formula(
                formula,
                self.__log.leader_state,
                self.__log.term,
                self.__log.last_log_index + 1,
            )

            await self.__append_entry(entry)

            logger.info(f"Committed new formula {formula} to log")

    @async_loop
    async def __assign_task(self, exponent: int = SUBINTERVAL_EXPONENT) -> None:
        await asyncio.sleep(2)

        if (formula := self.__log.current_formula) is None:
            logger.debug("No current formula to assign tasks for")
            return

        if not self.__task_queue:
            self.__task_queue = TaskQueue(formula, exponent)
            logger.info(f"Set {self.__task_queue} for new formula {formula}")

            await self.__set_new_completed_tasks(self.__task_queue.completed_tasks)

        if (task := self.__task_queue.next_task()) is None:
            return

        await self.__send_task(formula, task, exponent)

    async def __complete_task(self, task: int) -> None:
        entry = LogEntryFactory.complete_task(
            task,
            self.__log.leader_state,
            self.__log.term,
            self.__log.last_log_index + 1,
        )

        if not self.__task_queue:
            return

        self.__task_queue.complete_task(task)

        await self.__append_entry(entry)

    async def __reset_task_queue(self) -> None:
        self.__task_queue = None
        await self.__remove_current_formula()

    async def __set_new_completed_tasks(self, completed_tasks: list[bool]) -> None:
        entry = LogEntryFactory.set_completed_tasks(
            completed_tasks,
            self.__log.leader_state,
            self.__log.term,
            self.__log.last_log_index + 1,
        )

        await self.__append_entry(entry)

    async def __remove_current_formula(self) -> None:
        entry = LogEntryFactory.pop_formula(
            self.__log.leader_state, self.__log.term, self.__log.last_log_index + 1
        )

        await self.__append_entry(entry)
