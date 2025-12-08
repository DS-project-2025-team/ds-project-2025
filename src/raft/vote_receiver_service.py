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
from services.logger_service import logger
from utils.async_loop import async_loop


class VoteReceiverService(AbstractAsyncContextManager):
    def __init__(
        self, server: ServerAddress, node_id: UUID, producer: MessageProducer, log: Log
    ) -> None:
        self.__log: Log = log

        self.__producer: MessageProducer = producer
        self.__vote_consumer: MessageConsumer = (
            MessageConsumerFactory.vote_request_consumer(server, node_id)
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
    async def handle_vote(self) -> None:
        message = await self.__vote_consumer.receive()

        term = message.data["term"]
        candidate_id = UUID(message.data["candidate_id"])
        last_log_index = message.data["last_log_index"]
        last_log_term = message.data["last_log_term"]

        logger.info(f"Received vote request from {candidate_id} for term {term}")

        vote_granted = (
            term >= self.__log.term
            and self.__log.voted_for in (None, candidate_id)
            and self.__check_log_up_to_date(last_log_index, last_log_term)
        )

        if vote_granted:
            self.__log.voted_for = candidate_id
            logger.info(f"Voted for {candidate_id} in term {term}")
        else:
            logger.info(f"Did not vote for {candidate_id} in term {term}")

        await self.__send_vote(vote_granted)

    def __check_log_up_to_date(self, last_log_index: int, last_log_term: int) -> bool:
        """
        Returns whether the candidate's log is at least as up-to-date as node.
        """

        if last_log_term < self.__log.last_log_term:
            return False

        if (
            last_log_term == self.__log.last_log_term
            and last_log_index < self.__log.last_log_index
        ):
            return False

        return last_log_term > self.__log.last_log_term

    async def __send_vote(self, vote_granted: bool) -> None:
        payload = {
            "term": self.__log.term,
            "vote_granted": vote_granted,
        }

        await self.__producer.send(Topic.VOTE, payload)
