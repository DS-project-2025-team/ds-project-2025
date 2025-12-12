import asyncio
from collections.abc import Iterable
from contextlib import AbstractAsyncContextManager, suppress
from types import TracebackType
from typing import Literal, Self
from uuid import UUID

from config import SUBINTERVAL_EXPONENT
from entities.sat_formula import SatFormula
from entities.second import Second
from entities.server_address import ServerAddress
from entities.task_queue import TaskQueue
from network.message import Message
from network.message_consumer import MessageConsumer
from network.message_consumer_factory import MessageConsumerFactory
from network.message_producer import MessageProducer
from network.topic import Topic
from raft.entities.log import Log
from raft.entities.log_entry import LogEntry
from raft.entities.log_entry_factory import LogEntryFactory
from raft.roles.role import Role
from services.logger_service import logger
from utils.async_loop import async_loop
from utils.hash_sat_formula import hash_sat_formula


class Leader(AbstractAsyncContextManager):
    def __init__(
        self,
        log: Log,
        server: ServerAddress,
        node_id: UUID,
        producer: MessageProducer,
        task_queue: TaskQueue | None = None,
    ) -> None:
        self.__producer: MessageProducer = producer
        self.__input_consumer: MessageConsumer = MessageConsumerFactory.input_consumer(
            server,
        )
        self.__append_entries_consumer: MessageConsumer = (
            MessageConsumerFactory.append_entries_response_consumer(
                server=server, node_id=node_id
            )
        )
        self.__report_consumer: MessageConsumer = (
            MessageConsumerFactory.report_consumer(server=server)
        )

        self.__task_queue: TaskQueue | None = task_queue
        self.__log: Log = log
        self.__node_id: UUID = node_id

    async def __aenter__(self) -> Self:
        await self.__input_consumer.__aenter__()
        await self.__append_entries_consumer.__aenter__()
        await self.__report_consumer.__aenter__()

        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.__append_entries_consumer.__aexit__(exc_type, exc_value, traceback)
        await self.__input_consumer.__aexit__(exc_type, exc_value, traceback)
        await self.__report_consumer.__aexit__(exc_type, exc_value, traceback)

    async def run(self) -> Literal[Role.FOLLOWER]:
        try:
            async with asyncio.TaskGroup() as group:
                _task1 = group.create_task(self.__send_append_entries([]))
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
        """
        Receives one SAT formula.

        Raises:
            TimeoutError: If timeout is exceeded.
        """

        message = await self.__input_consumer.receive(timeout)
        input_ = message.data

        return SatFormula(input_["data"])

    async def __send_output(self, result: bool) -> None:
        logger.info(f"Computed result: {result}")

        payload = {
            "hash": hash(self.__task_queue),
            "result": result,
        }

        await self.__producer.send(Topic.OUTPUT, payload)

        logger.info(f"Sent result {result}")

    @async_loop
    async def __send_append_entries(self, entries: Iterable[LogEntry]) -> None:
        index_len = self.__log.entries.__len__()

        await self.__producer.send_and_wait(
            Topic.APPEND_ENTRIES,
            {
                "term": self.__log.term,
                "sender": str(self.__node_id),
                "entries": [entry.to_dict() for entry in entries],
            },
        )
        logger.debug(
            "Send event, last sent index: %s -> %s",
            self.__log.last_acked_index,
            index_len - 1,
        )
        self.__log.last_acked_index = index_len - 1

        await asyncio.sleep(2)

    async def __append_entry(self, entry: LogEntry) -> None:
        async with self.__log.append_lock:
            self.__log.append(entry)

            await self.__send_append_entries([entry])
            await self.__receive_append_entries_response()

            self.__log.commit()

    @async_loop
    async def __receive_append_entries_response(self) -> None:
        """
        Read messages via append_entries_response_consumer
        """

        message = await self.__append_entries_consumer.receive()
        await self.__handle_message(message)

    async def __send_task(self, formula: SatFormula, task: int, exponent: int) -> None:
        payload = {"formula": formula.to_list(), "task": task, "exponent": exponent}

        await self.__producer.send(Topic.ASSIGN, payload)
        logger.info(f"Assigned task {task} of formula {hash_sat_formula(formula)}")

    @async_loop
    async def __handle_report(self) -> None:
        message = await self.__report_consumer.receive()

        data = message.data

        if data["hash"] != hash(self.__task_queue):
            logger.debug(f"Received outdated REPORT with hash {data['hash']}")
            return

        await self.__complete_task(data["task"])

        satisfiable: bool = message.data["result"]

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

            async with self.__log.lock:
                self.__log.append(entry)

            self.__log.commit()

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

    async def __handle_message(self, message: Message) -> None:
        pass

    async def __complete_task(self, task: int) -> None:
        async with self.__log.lock:
            entry = LogEntryFactory.complete_task(
                task,
                self.__log.leader_state,
                self.__log.term,
                self.__log.last_log_index + 1,
            )

            if not self.__task_queue:
                return

            self.__task_queue.complete_task(task)

            self.__log.append(entry)

            self.__log.commit()

    async def __reset_task_queue(self) -> None:
        self.__task_queue = None
        await self.__remove_current_formula()

    async def __set_new_completed_tasks(self, completed_tasks: list[bool]) -> None:
        async with self.__log.lock:
            entry = LogEntryFactory.set_completed_tasks(
                completed_tasks,
                self.__log.leader_state,
                self.__log.term,
                self.__log.last_log_index + 1,
            )

            self.__log.append(entry)

            self.__log.commit()

    async def __remove_current_formula(self) -> None:
        async with self.__log.lock:
            entry = LogEntryFactory.pop_formula(
                self.__log.leader_state, self.__log.term, self.__log.last_log_index + 1
            )

            self.__log.append(entry)

            self.__log.commit()
