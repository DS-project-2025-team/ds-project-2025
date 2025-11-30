import asyncio

from entities.server_address import ServerAddress
from network.message_producer import MessageProducer
from logger_service import logger

async def main() -> None:
    server = ServerAddress("svm-11.cs.helsinki.fi", 9092)

    async with MessageProducer(server=server) as producer:
        while True:
            # produce
            await producer.send_and_wait("hello", {"data": "Hello, World!"})
            await producer.send_and_wait("hello", {"data": "a"})
            await producer.send_and_wait("hello", {"data": "b"})
            await producer.send_and_wait("hello", {"data": "c"})
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
