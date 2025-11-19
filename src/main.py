import logging

from entities.node import Node

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    node = Node()

    node.run()
