from typing import Self
from uuid import UUID

from raft.roles.role import Role


class ConsumerGroup(str):
    """
    Class representing Kafka consumer group.
    """

    @classmethod
    def leader(cls) -> Self:
        return cls(Role.LEADER)

    @classmethod
    def canditate(cls) -> Self:
        return cls(Role.CANDIDATE)

    @classmethod
    def follower(cls) -> Self:
        return cls(Role.FOLLOWER)

    @classmethod
    def node(cls, node_id: UUID) -> Self:
        return cls(node_id)
