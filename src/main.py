import asyncio

from entities.node import Node
from network.message_service import MessageService


async def main() -> None:
    async with MessageService("localhost", 9092) as message_service:
        node = Node(message_service=message_service)

    node.run()


if __name__ == "__main__":
    asyncio.run(main())
