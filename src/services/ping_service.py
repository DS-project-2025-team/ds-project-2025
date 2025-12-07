from contextlib import AbstractAsyncContextManager
from uuid import UUID

from entities.server_address import ServerAddress
from network.message_consumer import MessageConsumer
from network.message_consumer_factory import MessageConsumerFactory
from network.message_producer import MessageProducer


class PingService(AbstractAsyncContextManager):
    """
    Class for counting alive consumers, assuming one consumer per group.
    """

    def __init__(
        self,
        server: ServerAddress,
        node_id: UUID,
        count: int = 0,
    ) -> None:
        self.__count: int = count
        self.__producer: MessageProducer = MessageProducer(server)
        self.__consumer: MessageConsumer = (
            MessageConsumerFactory.ping_response_consumer(server, node_id)
        )
