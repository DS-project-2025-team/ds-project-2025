from uuid import UUID

from entities.server_address import ServerAddress
from network.message_consumer import MessageConsumer
from network.topic import Topic


class MessageConsumerFactory:
    @staticmethod
    def heartbeat_consumer(server: ServerAddress, node_id: UUID) -> MessageConsumer:
        return MessageConsumer(
            Topic.HEARTBEAT,
            server=server,
            groupid=str(node_id),
        )
