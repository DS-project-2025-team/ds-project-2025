import asyncio
import logging
from argparse import ArgumentParser

from entities.node import Node
from entities.server_address import ServerAddress
from logger_service import logger
from roles.role import Role


def init_parser() -> ArgumentParser:
    parser = ArgumentParser()

    parser.add_argument(
        "--role",
        type=str,
        help="Node role",
        default="FOLLOWER",
    )

    parser.add_argument(
        "--server",
        "-s",
        type=str,
        help="Kafka server",
        default="localhost",
    )

    parser.add_argument(
        "--port",
        "-p",
        type=int,
        help="Kafka server port",
        default=9092,
    )

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
    role = Role[args.role.upper()]
    kafka_server = ServerAddress(host=args.server, port=args.port)

    node = Node(server=kafka_server, role=role)

    await node.run()


if __name__ == "__main__":
    asyncio.run(main())
