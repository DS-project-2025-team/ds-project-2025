import asyncio

from services.message_service import MessageService


async def main() -> None:
    message_service = MessageService("localhost", 9092)

    # await message_service.stop()

    await message_service.start()

    await message_service.send("hello", b"Hello, World!")
    messages = await message_service.receive()
    await message_service.stop()

    print(messages)


if __name__ == "__main__":
    asyncio.run(main())
