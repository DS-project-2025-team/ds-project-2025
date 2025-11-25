import asyncio

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from services.message_service import MessageService


async def main() -> None:
    producer = AIOKafkaProducer(bootstrap_servers="localhost:9092")
    consumer = AIOKafkaConsumer("hello", bootstrap_servers="localhost:9092")

    message_service = MessageService(producer=producer, consumer=consumer)

    # await message_service.stop()

    await message_service.start()

    await message_service.send("hello", b"Hello, World!")
    messages = await message_service.receive()
    await message_service.stop()

    print(messages)


if __name__ == "__main__":
    asyncio.run(main())
