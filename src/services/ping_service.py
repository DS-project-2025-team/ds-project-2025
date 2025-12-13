import asyncio
from contextlib import AbstractAsyncContextManager, suppress
from types import TracebackType
from typing import TYPE_CHECKING, Self
from uuid import UUID

from entities.second import Second
from entities.server_address import ServerAddress
from network.message_consumer import MessageConsumer
from network.message_consumer_factory import MessageConsumerFactory
from network.message_producer import MessageProducer
from network.topic import Topic
from raft.raft_config import RaftConfig
from services.logger_service import logger
from utils.async_loop import async_loop

if TYPE_CHECKING:
    from raft.node import Node
class PingService(AbstractAsyncContextManager):
    """
    Class for counting alive consumers, assuming one consumer per group.
    """

    def __init__(
        self,
        server: ServerAddress,
        node_id: UUID,
        producer: MessageProducer,
        timeout: Second = Second(5),
        raft_config: RaftConfig | None = None,
    ) -> None:
        self.__id: UUID = node_id
        self.__timeout: Second = timeout
        self.__raft_config: RaftConfig = raft_config or RaftConfig()
        self.__producer: MessageProducer = producer
        self.__consumer: MessageConsumer = (
            MessageConsumerFactory.ping_response_consumer(server, node_id)
        )

    async def __aenter__(self) -> Self:
        self.__consumer = await self.__consumer.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        await self.__consumer.__aexit__(exc_type, exc_value, traceback)

    async def count_consumers(self) -> RaftConfig:
        """
        Counts alive consumers.

        Returns:
            int: Number of alive consumers
        """
        payload = {
            "sender": str(self.__id),
        }

        await self.__producer.send(Topic.PING, payload)

        with suppress(TimeoutError):
            await asyncio.wait_for(self.receive_response(), timeout=self.__timeout)

        return self.__raft_config


    @async_loop
    async def receive_response(self) -> None:
        message = await self.__consumer.receive()

        receiver = UUID(message.data["receiver"])

        if receiver != self.__id:
            return

        server = ServerAddress(
                    message.data["connect"]["host"],
                    message.data["connect"]["port"])
        uuid = message.data["receiver"]

        await self.__raft_config.add_node(uuid, server)
