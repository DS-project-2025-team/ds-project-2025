from contextlib import AbstractAsyncContextManager
from types import TracebackType
from typing import Self
from uuid import UUID

from entities.server_address import ServerAddress
from network.message_consumer import MessageConsumer
from network.message_consumer_factory import MessageConsumerFactory
from network.message_producer import MessageProducer
from network.topic import Topic
from raft.entities.log import Log
from utils.async_loop import async_loop


class VoteReceiverService(AbstractAsyncContextManager):
    def __init__(
        self, server: ServerAddress, node_id: UUID, producer: MessageProducer, log: Log
    ) -> None:
        self.__log: Log = log

        self.__producer: MessageProducer = producer
        self.__vote_consumer: MessageConsumer = MessageConsumerFactory.vote_consumer(
            server, node_id
        )

    async def __aenter__(self) -> Self:
        await self.__vote_consumer.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.__vote_consumer.__aexit__(exc_type, exc_value, traceback)

    @async_loop
    async def __handle_vote(self) -> None:
        message = await self.__vote_consumer.receive()
        term = message.data["term"]
        candidate_id = message.data["candidate_id"]
        last_log_index = message.data["last_log_index"]
        last_log_term = message.data["last_log_term"]

        if term < self.__log.term:
            await self.__reject_vote()
            return

    async def __reject_vote(self) -> None:
        payload = {
            "term": self.__log.term,
            "vote_granted": False,
        }
        await self.__producer.send(Topic.VOTE, payload)
