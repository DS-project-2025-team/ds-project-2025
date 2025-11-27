from entities.node import Node
from services.message_service import MessageService

if __name__ == "__main__":
    message_service = MessageService("localhost", 9092)
    node = Node(message_service=message_service)

    node.run()
