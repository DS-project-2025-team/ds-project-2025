import asyncio

from network.message_service import MessageService
from logger_service import logger


async def main() -> None:
    async with MessageService("svm-11.cs.helsinki.fi", 9092, "hello_group") as message_service:
        # subscribe to topic
        message_service.subscribe("hello")
        await consume_loop(message_service)

async def consume_loop(message_service: MessageService) -> None:
    try:
        while True:
            try:
                messages = await message_service.receive()
                await asyncio.sleep(1)

            except Exception as e:
                logger.error("Error while consuming: %r", e)
                await asyncio.sleep(1)

    
    finally:
        logger.info("Consumer receive loop exiting")
        await message_service.stop()


if __name__ == "__main__":
    asyncio.run(main())
