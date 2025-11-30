import asyncio
from argparse import ArgumentParser

from entities.node import Node
from network.message_service import MessageService
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

    return parser


async def main() -> None:
    parser = init_parser()
    args = parser.parse_args()

    role = Role[args.role.upper()]
    server: str = args.server

    async with MessageService(server, 9092) as message_service:
        node = Node(message_service=message_service, role=role)

    await node.run()


if __name__ == "__main__":
    asyncio.run(main())
