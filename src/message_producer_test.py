import asyncio

from network.message_service import MessageService
from logger_service import logger

async def main() -> None:
    async with MessageService("svm-11.cs.helsinki.fi", 9092, "hello_group") as message_service:
        while True:
            # produce
            metadata = await message_service.send_and_wait("hello", {"data": "Hello, World!"})
            metadata = await message_service.send_and_wait("hello", {"data": "a"})
            metadata = await message_service.send_and_wait("hello", {"data": "b"})
            metadata = await message_service.send_and_wait("hello", {"data": "c"})
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
