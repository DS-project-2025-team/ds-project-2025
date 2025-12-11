from uuid import UUID

from entities.server_address import ServerAddress
from network.consumer_group import ConsumerGroup
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
            group=ConsumerGroup.node(node_id),
            offset_reset="latest",
        )

    @staticmethod
    def append_entries_response_consumer(
        server: ServerAddress, node_id: UUID
    ) -> MessageConsumer:
        return MessageConsumerFactory.multicast_consumer(
            Topic.APPEND_ENTRIES_RESPONSE,
            server=server,
            node_id=node_id,
        )

    @staticmethod
    def append_entries_consumer(server: ServerAddress, node_id: UUID) -> MessageConsumer:
        return MessageConsumerFactory.multicast_consumer(
            Topic.APPEND_ENTRIES, server=server, node_id=node_id
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
        return MessageConsumer(
            Topic.INPUT,
            server=server,
            group=ConsumerGroup.leader(),
            offset_reset="latest",
        )

    @staticmethod
    def client_consumer(server: ServerAddress, node_id: UUID) -> MessageConsumer:
        return MessageConsumerFactory.multicast_consumer(
            Topic.OUTPUT, server=server, node_id=node_id
        )

    @staticmethod
    def report_consumer(server: ServerAddress) -> MessageConsumer:
        return MessageConsumer(
            Topic.REPORT,
            server=server,
            group=ConsumerGroup.leader(),
            offset_reset="latest",
        )

    @staticmethod
    def assign_consumer(server: ServerAddress) -> MessageConsumer:
        return MessageConsumer(
            Topic.ASSIGN,
            server=server,
            group=ConsumerGroup.follower(),
            offset_reset="latest",
        )

    @staticmethod
    def ping_consumer(server: ServerAddress, node_id: UUID) -> MessageConsumer:
        return MessageConsumerFactory.multicast_consumer(
            Topic.PING, server=server, node_id=node_id
        )

    @staticmethod
    def ping_response_consumer(server: ServerAddress, node_id: UUID) -> MessageConsumer:
        return MessageConsumerFactory.multicast_consumer(
            Topic.PING_RESPONSE, server=server, node_id=node_id
        )
