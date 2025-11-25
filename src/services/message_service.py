from aiokafka import AIOKafkaProducer


class MessageService:
    def __init__(self, producer: AIOKafkaProducer) -> None:
        self.__producer: AIOKafkaProducer = producer

    async def start(self) -> None:
        await self.__producer.start()
