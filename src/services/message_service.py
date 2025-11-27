from aiokafka import AIOKafkaConsumer, AIOKafkaProducer


class MessageService:
    def __init__(
        self,
        server: str,
        port: int = 9092,
    ) -> None:
        self.__producer: AIOKafkaProducer = AIOKafkaProducer(
            bootstrap_servers=f"{server}:{port}"
        )
        self.__consumer: AIOKafkaConsumer = AIOKafkaConsumer(
            "hello", bootstrap_servers=f"{server}:{port}"
        )

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
