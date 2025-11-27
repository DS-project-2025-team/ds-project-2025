import asyncio

from services.message_service import MessageService


async def main() -> None:
    async with MessageService("localhost", 9092) as message_service:
        await message_service.send("hello", b"Hello, World!")
        messages = await message_service.receive()

    print(messages)


if __name__ == "__main__":
    asyncio.run(main())
