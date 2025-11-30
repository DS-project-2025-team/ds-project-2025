import asyncio

from entities.server_address import ServerAddress
from network.message_consumer import MessageConsumer
from network.message_producer import MessageProducer


async def main() -> None:
    server = ServerAddress("localhost", 9092)

    async with (
        MessageConsumer("hello", server=server, groupid="hello_group") as consumer,
        MessageProducer(server=server) as producer,
    ):
        for i in range(1, 10):
            # produce
            await producer.send("hello", {"data": "Hello, World!"})
            await producer.send("hello", {"data": "a"})
            await producer.send("hello", {"data": "b"})
            await producer.send("hello", {"data": "c"})
            await asyncio.sleep(1)
            # consume
            messages = await consumer.receive()
            # commit (save offset)
            await consumer.commit()
            # print
            for tp, msgs in messages.items():
                for msg in msgs:
                    print(
                        f"topic={msg.topic}, "
                        f"partition={msg.partition}, "
                        f"offset={msg.offset}, "
                        f"value={msg.value}"
                    )


if __name__ == "__main__":
    asyncio.run(main())
