import asyncio
from argparse import ArgumentParser

from entities.node import Node
from network.message_service import MessageService
from network.topic import Topic
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

    return parser


async def main() -> None:
    parser = init_parser()
    args = parser.parse_args()

    role = Role[args.role.upper()]
    server: str = args.server
    port: int = args.port

    async with MessageService(server, port) as message_service:

        await node.run()


if __name__ == "__main__":
    asyncio.run(main())
