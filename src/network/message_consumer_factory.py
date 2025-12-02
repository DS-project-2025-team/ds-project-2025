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
        return MessageConsumer(
            Topic.HEARTBEAT,
            server=server,
            groupid=str(node_id),
        )

    @staticmethod
    def vote_request_consumer(server: ServerAddress, node_id: UUID) -> MessageConsumer:
        return MessageConsumer(
            Topic.VOTE_REQUEST,
            server=server,
            groupid=str(node_id),
        )

    @staticmethod
    def vote_consumer(server: ServerAddress, node_id: UUID) -> MessageConsumer:
        return MessageConsumer(
            Topic.VOTE,
            server=server,
            groupid=str(node_id),
        )
