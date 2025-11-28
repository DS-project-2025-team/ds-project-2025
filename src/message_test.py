import asyncio

from network.message_service import MessageService


async def main() -> None:
    async with MessageService("localhost", 9092) as message_service:
        await message_service.subscribe("hello")

        await message_service.send("hello", {"data": "Hello, World!"})

        messages = await message_service.receive()

    print(messages)


if __name__ == "__main__":
    asyncio.run(main())
