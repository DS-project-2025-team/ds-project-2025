import asyncio
import random
from contextlib import AbstractAsyncContextManager
from types import TracebackType
from typing import Literal, Self
from uuid import UUID

from entities.sat_formula import SatFormula
from entities.second import Second
from entities.server_address import ServerAddress
from network.message_consumer import MessageConsumer
from network.message_consumer_factory import MessageConsumerFactory
from network.message_producer import MessageProducer
from network.topic import Topic
from roles.role import Role
from services.logger_service import logger
from services.worker_service import WorkerService
from utils.async_loop import async_loop
from utils.hash_sat_formula import hash_sat_formula


class Follower(AbstractAsyncContextManager):
    def __init__(
        self,
        server: ServerAddress,
        node_id: UUID,
        election_timeout: Second | None = None,
        worker: WorkerService | None = None,
    ) -> None:
        self.__producer: MessageProducer = MessageProducer(server=server)
        self.__appendentry_consumer: MessageConsumer = (
            MessageConsumerFactory.appendentry_consumer(server=server, node_id=node_id)
        )
        self.__assign_consumer: MessageConsumer = (
            MessageConsumerFactory.assign_consumer(server=server)
        )
        self.__worker: WorkerService = worker or WorkerService()

        self.__election_timeout: Second = election_timeout or Second(
            10 + random.randint(0, 5)
        )
        self.__node_id = node_id

    async def __aenter__(self) -> Self:
        await self.__producer.__aenter__()
        await self.__appendentry_consumer.__aenter__()
        await self.__assign_consumer.__aenter__()
        self.__worker.__enter__()

        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.__producer.__aexit__(exc_type, exc_value, traceback)
        await self.__appendentry_consumer.__aexit__(exc_type, exc_value, traceback)
        await self.__assign_consumer.__aexit__(exc_type, exc_value, traceback)
        self.__worker.__exit__(exc_type, exc_value, traceback)

    async def run(self) -> Literal[Role.CANDIDATE]:
        try:
            async with asyncio.TaskGroup() as group:
                group.create_task(self.__handle_appendentry())
                group.create_task(self.__handle_assign())

                logger.info("Follower is running")
        except TimeoutError:
            logger.warning("Missing heartbeat, election timeout elapsed.")

        logger.info("Changing role to CANDIDATE")
        return Role.CANDIDATE

    @async_loop
    async def __handle_appendentry(self) -> None:
        message = await self.__appendentry_consumer.receive(self.__election_timeout)
        await self.__appendentry_consumer.commit()

        logger.debug(f"Received {message.topic}")

        # send response with received message offset
        await self.__producer.send(
            Topic.APPENDENTRY_RESPONSE,
            {
                "responder_uuid": str(self.__node_id),
                "original_offset": message.offset,
            },
        )

    @async_loop
    async def __handle_assign(self) -> None:
        message = await self.__assign_consumer.receive()

        data = message.data

        logger.info(f"Received work: {data}")

        formula: SatFormula = SatFormula(data["formula"])
        task: int = data["task"]
        exponent: int = data["exponent"]

        result = await self.__worker.run_task(
            formula,
            task,
            exponent,
        )

        await self.__send_result(formula, task, result)

    async def __send_result(self, formula: SatFormula, task: int, result: bool) -> None:
        payload = {
            "hash": hash_sat_formula(formula),
            "task": task,
            "result": result,
        }

        await self.__producer.send(Topic.REPORT, payload)

        logger.info(f"Sent result for task {task}: {result}")
