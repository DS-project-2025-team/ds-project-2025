from aiokafka import AIOKafkaProducer


class MessageService:
    def __init__(self, producer: AIOKafkaProducer) -> None:
        self.__producer: AIOKafkaProducer = producer

    async def send(self, topic: str, message: bytes) -> None:
        await self.__producer.send_and_wait(topic, message)

    async def start(self) -> None:
        await self.__producer.start()
