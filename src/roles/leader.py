import asyncio
from contextlib import AbstractAsyncContextManager, suppress
from types import TracebackType
from typing import Literal, Self
from uuid import UUID

from config import SUBINTERVAL_EXPONENT
from entities.log_entry_factory import LogEntryFactory
from entities.raft_log import RaftLog
from entities.sat_formula import SatFormula
from entities.second import Second
from entities.server_address import ServerAddress
from network.message import Message
from network.message_consumer import MessageConsumer
from network.message_consumer_factory import MessageConsumerFactory
from network.message_producer import MessageProducer
from network.topic import Topic
from roles.role import Role
from services.logger_service import logger
from services.task_scheduler_service import TaskSchedulerService
from utils.async_loop import async_loop


class Leader(AbstractAsyncContextManager):
    def __init__(
        self,
        log: RaftLog,
        server: ServerAddress,
        node_id: UUID,
        task_scheduler: TaskSchedulerService | None = None,
    ) -> None:
        self.__producer: MessageProducer = MessageProducer(server=server)
        self.__input_consumer: MessageConsumer = MessageConsumerFactory.input_consumer(
            server,
            node_id,
        )
        self.__heartbeat_consumer: MessageConsumer = (
            MessageConsumerFactory.heartbeat_response_consumer(
                server=server, node_id=node_id
            )
        )
        self.__report_consumer: MessageConsumer = (
            MessageConsumerFactory.report_consumer(server=server)
        )

        self.__scheduler: TaskSchedulerService | None = task_scheduler
        self.__log: RaftLog = log
        self.__node_id: UUID = node_id

    async def __aenter__(self) -> Self:
        await self.__producer.__aenter__()
        await self.__input_consumer.__aenter__()
        await self.__heartbeat_consumer.__aenter__()
        await self.__report_consumer.__aenter__()

        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.__heartbeat_consumer.__aexit__(exc_type, exc_value, traceback)
        await self.__producer.__aexit__(exc_type, exc_value, traceback)
        await self.__input_consumer.__aexit__(exc_type, exc_value, traceback)
        await self.__report_consumer.__aexit__(exc_type, exc_value, traceback)

    async def run(self) -> Literal[Role.FOLLOWER]:
        try:
            async with asyncio.TaskGroup() as group:
                _task1 = group.create_task(self.__send_heartbeat())
                _task2 = group.create_task(self.__receive_heartbeat_response())
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
            "hash": hash(self.__scheduler),
            "result": result,
        }

        await self.__producer.send(Topic.OUTPUT, payload)

        logger.info(f"Sent result {result}")

    @async_loop
    async def __send_heartbeat(self) -> None:
        await self.__producer.send_and_wait(
            Topic.HEARTBEAT, {"sender": str(self.__node_id)}
        )

        logger.debug(f"Sent {Topic.HEARTBEAT}")

        await asyncio.sleep(2)

    @async_loop
    async def __receive_heartbeat_response(self) -> None:
        """
        Read messages via heartbeat_response_consumer
        """

        message = await self.__heartbeat_consumer.receive()
        await self.__handle_message(message)

    async def __send_task(self, formula: SatFormula, task: int, exponent: int) -> None:
        payload = {"formula": formula.to_list(), "task": task, "exponent": exponent}

        await self.__producer.send(Topic.ASSIGN, payload)
        logger.info(f"Assigned task {task} of formula {formula}")

    @async_loop
    async def __handle_report(self) -> None:
        message = await self.__report_consumer.receive()

        data = message.data

        if data["hash"] != hash(self.__scheduler):
            logger.debug(f"Received outdated REPORT with hash {data['hash']}")
            return

        self.__complete_task(data["task"])

        satisfiable: bool = message.data["result"]

        if satisfiable:
            await self.__send_output(satisfiable)
            self.__remove_current_formula()
            return

        if self.__scheduler and self.__scheduler.done():
            await self.__send_output(False)
            self.__remove_current_formula()

    @async_loop
    async def __handle_input(self, timeout: Second) -> None:
        with suppress(TimeoutError):
            formula = await self.__receive_input(timeout)

            logger.info(f"Received new SAT formula: {formula}")

            entry = LogEntryFactory.add_formula(self.__log.term, formula)

            self.__log.append(entry)
            self.__log.commit()

            logger.info(f"Committed new formula {formula} to log")

    @async_loop
    async def __assign_task(self, exponent: int = SUBINTERVAL_EXPONENT) -> None:
        await asyncio.sleep(1)

        if (formula := self.__log.current_formula) is None:
            logger.info("No current formula to assign tasks for")
            return

        if not self.__scheduler:
            self.__scheduler = TaskSchedulerService(formula, exponent)
            logger.info(f"Set {self.__scheduler} for new formula {formula}")

            self.__set_new_completed_tasks(self.__scheduler.completed_tasks)

        if (task := self.__scheduler.next_task()) is None:
            return

        await self.__send_task(formula, task, exponent)

    async def __handle_message(self, message: Message) -> None:
        logger.debug(f"Received {message.topic}")

    def __complete_task(self, task: int) -> None:
        entry = LogEntryFactory.complete_task(self.__log.term, task)

        if not self.__scheduler:
            return

        self.__scheduler.complete_task(task)

        self.__log.append(entry)
        self.__log.commit()

    def __set_new_completed_tasks(self, completed_tasks: list[bool]) -> None:
        entry = LogEntryFactory.set_completed_tasks(self.__log.term, completed_tasks)

        self.__log.append(entry)
        self.__log.commit()

    def __remove_current_formula(self) -> None:
        entry = LogEntryFactory.pop_formula(self.__log.term)

        self.__log.append(entry)
        self.__log.commit()
