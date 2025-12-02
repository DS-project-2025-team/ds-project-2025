from contextlib import AbstractAsyncContextManager
from types import TracebackType
from typing import Self

from entities.sat_formula import SatFormula
from entities.server_address import ServerAddress
from network.message_consumer import MessageConsumer
from network.message_producer import MessageProducer
from network.topic import Topic


class Client(AbstractAsyncContextManager):
    """
    Class for sending SAT formulas into the system and receiving the result.
    """

    def __init__(self, server: ServerAddress) -> None:
        self.__producer = MessageProducer(server)
        self.__consumer = MessageConsumer(Topic.OUTPUT, server=server)

    async def __aenter__(self) -> Self:
        await self.__consumer.__aenter__()
        await self.__producer.__aenter__()

        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.__producer.__aexit__(exc_type, exc_value, traceback)
        await self.__consumer.__aexit__(exc_type, exc_value, traceback)

    async def __send(self, formula: SatFormula) -> None:
        await self.__producer.send_and_wait(Topic.INPUT, {"data": formula})

    async def __wait_for_result(self, id_: int) -> bool:
        while True:
            message = await self.__consumer.receive()

            if message["hash"] == id_:
                return message["result"]

    async def input(self, formula: SatFormula) -> bool:
        """
        Sends SAT formula as input and returns the result.

        Args:
            formula (SatFormula): SAT formula

        Returns:
            bool: Satisfiability of the formula
        """
        id_ = hash(formula)

        await self.__send(formula)
        return await self.__wait_for_result(id_)
