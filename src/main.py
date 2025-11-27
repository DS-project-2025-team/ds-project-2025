import asyncio

from entities.node import Node
from services.message_service import MessageService


async def main() -> None:
    message_service = MessageService("localhost", 9092)
    node = Node(message_service=message_service)

    node.run()


if __name__ == "__main__":
    asyncio.run(main())
