import asyncio

from network.message_service import MessageService


async def main() -> None:
    async with MessageService("localhost", 9092, 'hello_group') as message_service:
        # subscribe to topic
        await message_service.subscribe("hello")
        for i in range (1, 10):
            # produce
            await message_service.send("hello", {"data": "Hello, World!"})
            await message_service.send("hello", {"data": "a"})
            await message_service.send("hello", {"data": "b"})
            await message_service.send("hello", {"data": "c"})
            await asyncio.sleep(1)
            # consume
            messages = await message_service.receive()
            # commit (save offset)
            await message_service.commit()
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
