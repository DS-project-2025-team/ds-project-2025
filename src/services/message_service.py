from aiokafka import AIOKafkaConsumer, AIOKafkaProducer


class MessageService:
    def __init__(self, producer: AIOKafkaProducer, consumer: AIOKafkaConsumer) -> None:
        self.__producer: AIOKafkaProducer = producer
        self.__consumer: AIOKafkaConsumer = consumer

    async def send(self, topic: str, message: bytes) -> None:
        await self.__producer.send_and_wait(topic, message)

    async def receive(self) -> str:
        message = await self.__consumer.getone()

        return str(message.value)

    async def start(self) -> None:
        await self.__producer.start()
        await self.__consumer.start()

    async def stop(self) -> None:
        await self.__producer.stop()
        await self.__consumer.stop()
