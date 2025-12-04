import asyncio
import random
from contextlib import AbstractAsyncContextManager
from re import S
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
from utils.async_loop import async_loop
from utils.check_sat import check_sat_formula
from utils.hash_sat_formula import hash_sat_formula
from utils.task import get_subinterval


class Follower(AbstractAsyncContextManager):
    def __init__(
        self,
        server: ServerAddress,
        node_id: UUID,
        election_timeout: Second | None = None,
    ) -> None:
        self.__producer: MessageProducer = MessageProducer(server=server)
        self.__heartbeat_consumer: MessageConsumer = (
            MessageConsumerFactory.heartbeat_consumer(server=server, node_id=node_id)
        )
        self.__assign_consumer: MessageConsumer = (
            MessageConsumerFactory.assign_consumer(server=server)
        )

        self.__election_timeout: Second = election_timeout or Second(
            10 + random.randint(0, 5)
        )
        self.__node_id = node_id

    async def __aenter__(self) -> Self:
        await self.__producer.__aenter__()
        await self.__heartbeat_consumer.__aenter__()
        await self.__assign_consumer.__aenter__()

        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.__producer.__aexit__(exc_type, exc_value, traceback)
        await self.__heartbeat_consumer.__aexit__(exc_type, exc_value, traceback)
        await self.__assign_consumer.__aexit__(exc_type, exc_value, traceback)

    async def run(self) -> Literal[Role.CANDIDATE]:
        try:
            async with asyncio.TaskGroup() as group:
                group.create_task(self.__handle_heartbeat())

        except TimeoutError:
            logger.warning("Missing heartbeat, election timeout elapsed.")

        logger.info("Changing role to CANDIDATE")
        return Role.CANDIDATE

    @async_loop
    async def __handle_heartbeat(self) -> None:
        message = await self.__heartbeat_consumer.receive(self.__election_timeout)
        await self.__heartbeat_consumer.commit()

        logger.debug(f"Received {message.topic}")

        # send response with received message offset
        await self.__producer.send(
            Topic.HEARTBEAT_RESPONSE,
            {
                "responder_uuid": str(self.__node_id),
                "original_offset": message.offset,
            },
        )

    @async_loop
    async def __handle_assign(self) -> None:
        message = await self.__assign_consumer.receive()

        data = message.data

        logger.debug(f"Received work: {data}")

        formula: SatFormula = SatFormula(data["formula"])
        task: int = data["task"]
        exponent: int = data["exponent"]

        satisfiable = self.__compute(formula, task, exponent)

        await self.__send_result(formula, task, satisfiable)

    def __compute(self, formula: SatFormula, task: int, exponent: int) -> bool:
        begin, end = get_subinterval(2**exponent, task)
        return check_sat_formula(formula, begin, end)

    async def __send_result(self, formula: SatFormula, task: int, result: bool) -> None:
        payload = {
            "hash": hash_sat_formula(formula),
            "task": task,
            "result": result,
        }

        await self.__producer.send(Topic.REPORT, payload)

        logger.debug(f"Sent result for task {task}: {result}")
