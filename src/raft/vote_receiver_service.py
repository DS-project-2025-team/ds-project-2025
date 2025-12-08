from uuid import UUID

from entities.server_address import ServerAddress
from network.message_consumer import MessageConsumer
from network.message_consumer_factory import MessageConsumerFactory
from network.message_producer import MessageProducer
from utils.async_loop import async_loop


class VoteReceiverService:
    def __init__(
        self, server: ServerAddress, node_id: UUID, producer: MessageProducer
    ) -> None:
        self.__producer: MessageProducer = producer
        self.__vote_consumer: MessageConsumer = MessageConsumerFactory.vote_consumer(
            server, node_id
        )

    @async_loop
    async def __handle_vote(self) -> None:
        message = await self.__vote_consumer.receive()
        sender = message.data["sender"]
        term = message.data["term"]
