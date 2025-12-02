from uuid import UUID

from entities.server_address import ServerAddress
from network.message_consumer import MessageConsumer
from network.topic import Topic


class MessageConsumerFactory:
    @staticmethod
    def multicast_consumer(
        *topics: Topic, server: ServerAddress, node_id: UUID
    ) -> MessageConsumer:
        return MessageConsumer(
            *topics,
            server=server,
            groupid=str(node_id),
        )

    @staticmethod
    def heartbeat_consumer(server: ServerAddress, node_id: UUID) -> MessageConsumer:
        return MessageConsumerFactory.multicast_consumer(
            Topic.HEARTBEAT, server=server, node_id=node_id
        )

    @staticmethod
    def vote_request_consumer(server: ServerAddress, node_id: UUID) -> MessageConsumer:
        return MessageConsumerFactory.multicast_consumer(
            Topic.VOTE_REQUEST, server=server, node_id=node_id
        )

    @staticmethod
    def vote_consumer(server: ServerAddress, node_id: UUID) -> MessageConsumer:
        return MessageConsumerFactory.multicast_consumer(
            Topic.VOTE, server=server, node_id=node_id
        )

    @staticmethod
    def input_consumer(server: ServerAddress) -> MessageConsumer:
        return MessageConsumer(Topic.INPUT, server=server)
