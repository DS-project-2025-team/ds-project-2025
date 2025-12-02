import asyncio
import logging
from argparse import ArgumentParser

from entities.server_address import ServerAddress
from logger_service import logger
from network.message_producer import MessageProducer


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

    async with MessageProducer(server=server) as producer:
        #while True:
        for i in range(10000):
            # produce
            await producer.send("hello", {"data": "Hello, World!"})
            await producer.send("hello", {"data": "a"})
            await producer.send("hello", {"data": "b"})
            await producer.send("hello", {"data": "c"})
            """ Just flood and quit """
            #await asyncio.sleep(1)

        print("sent ", i,"messages\n")

if __name__ == "__main__":
    asyncio.run(main())
