from uuid import UUID

from entities.server_address import ServerAddress
from network.message_consumer import MessageConsumer
from network.message_consumer_factory import MessageConsumerFactory
from network.message_producer import MessageProducer


class LeaderMessager:
    """
    Class for handling Leader messaging.
    """

    def __init__(
        self,
        server: ServerAddress,
        node_id: UUID,
        producer: MessageProducer,
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
