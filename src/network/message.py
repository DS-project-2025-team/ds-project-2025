from dataclasses import dataclass
from typing import Any, Self

from aiokafka import ConsumerRecord

from network.topic import Topic


@dataclass
class Message:
    """
    A typed wrapper around aiokafka.ConsumerRecord.
    Represents a message received from Kafka.
    """

    topic: Topic
    data: dict[str, Any]
    partition: int
    offset: int

    def __new__(cls, record: ConsumerRecord) -> Self:
        return cls(
            topic=Topic(record.topic),
            data=record.value,  # type: ignore
            partition=record.partition,
            offset=record.offset,
        )
