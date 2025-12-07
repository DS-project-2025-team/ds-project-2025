import asyncio
import logging
from argparse import ArgumentParser

from entities.server_address import ServerAddress
from network.message_consumer import MessageConsumer
from services.logger_service import logger


def init_parser() -> ArgumentParser:
    parser = ArgumentParser()

    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level",
    )

    return parser


async def main() -> None:
    parser = init_parser()
    args = parser.parse_args()
    level = getattr(logging, args.log_level.upper())
    logger.set_level(level)
    server = ServerAddress("svm-11.cs.helsinki.fi", 9092)

    async with MessageConsumer("hello", server=server, group="hello_group") as consumer:
        await consume_loop(consumer)


async def consume_loop(message_service: MessageConsumer) -> None:
    try:
        while True:
            try:
                await message_service.receive_many_and_log()

            except Exception as e:
                logger.error("Error while consuming: %r", e)

    finally:
        logger.info("Consumer receive loop exiting")
        await message_service.stop()


if __name__ == "__main__":
    asyncio.run(main())
