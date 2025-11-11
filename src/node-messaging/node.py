import argparse
import asyncio
import json
import logging
import os
import sys
from collections.abc import Awaitable, Callable
from typing import Any

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

print("ARGV:", sys.argv)

# ---------------------------
# Debug logging to stdout
# ---------------------------
def setup_logging(node_id: str) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [" + node_id + "] %(message)s",
    )


# ---------------------------
# Dispatcher
# ---------------------------
Handler = Callable[[dict[str, Any]], Awaitable[None]]

class Dispatcher:
    def __init__(self) -> None:
        self._handlers: dict[str, Handler] = {}

    def on(self, msg_type: str) -> Callable[[Handler], Handler]:
        def deco(fn: Handler) -> Handler:
            self._handlers[msg_type] = fn
            return fn
        return deco

    async def dispatch(self, msg_type: str, payload: dict[str, Any]) -> None:
        h = self._handlers.get(msg_type)
        if h is None:
            logging.warning("ei handleria tyypille %s, payload=%r", msg_type, payload)
            return
        await h(payload)


dispatcher = Dispatcher()


# ---------------------------
# Message
# ---------------------------

class Envelope(dict):
    @property
    def type(self) -> str:
        return self["type"]

    @property
    def payload(self) -> dict[str, Any]:
        return self["payload"]


# ---------------------------
# Class Node
# ---------------------------

class Node:
    def __init__(
        self,
        node_id: str,
        peers: list[str],
        bootstrap_servers: list[str],
        topic: str = "events",
    ) -> None:
        self.node_id = node_id
        self.peers = peers
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self._producer: AIOKafkaProducer | None = None
        self._consumer: AIOKafkaConsumer | None = None

    async def start(self) -> None:
        logging.info("Start the node, bootstrap=%r", self.bootstrap_servers)

        # Producer
        self._producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            acks="all",
            enable_idempotence=True,
            # Older aiokafka-version doesn't have
            # max_in_flight_requests_per_connection parameter
            #max_in_flight_requests_per_connection=1,
        )

        await self._producer.start()
        logging.info("Producer is running")

        # Consumer
        self._consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=f"grp-{self.node_id}",
            enable_auto_commit=False,
            auto_offset_reset="earliest",
            max_poll_records=1,
        )
        await self._consumer.start()
        logging.info("Consumer is running and listening ID: %s", self.node_id)

        # Start listen loop
        asyncio.create_task(self._consume_loop())

    async def stop(self) -> None:
        logging.info("Stopping the node...")
        if self._consumer:
            await self._consumer.stop()
        if self._producer:
            await self._producer.stop()
        logging.info("Node is stopped")

    async def _consume_loop(self) -> None:
        assert self._consumer is not None
        try:
            async for msg in self._consumer:
                # Filter messages by node id
                if msg.key is None or msg.key.decode() != self.node_id:
                    await self._consumer.commit()
                    continue

                try:
                    env = Envelope(json.loads(msg.value))
                except Exception as e:
                    logging.error("Error decoding the message: %s", e)
                    await self._consumer.commit()
                    continue

                logging.info("Recv <- type=%s payload=%r", env.type, env.payload)
                await dispatcher.dispatch(env.type, env.payload)
                await self._consumer.commit()
        except asyncio.CancelledError:
            pass

    async def send(self, to_node: str, msg_type: str, payload: dict[str, Any]) -> None:
        if self._producer is None:
            raise RuntimeError("Producer is not running")

        env = Envelope(type=msg_type, payload=payload)
        data = json.dumps(env).encode("utf-8")

        await self._producer.send_and_wait(
            self.topic,
            value=data,
            key=to_node.encode("utf-8"),
        )
        logging.info("Send -> %s type=%s payload=%r", to_node, msg_type, payload)


# ---------------------------
# Handler example
# ---------------------------
@dispatcher.on("ping")
async def handle_ping(payload: dict[str, Any]) -> None:
    logging.info("Process ping from=%r seq=%r", payload.get("from"), payload.get("seq"))


# ---------------------------
# async_main + main
# ---------------------------
async def async_main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--node-id", required=True)
    parser.add_argument("--peer", nargs="+", default=[])
    parser.add_argument(
        "--bootstrap",
        default=os.getenv(
            "KAFKA_BOOT",
            "localhost:9092",
        ),
    )

    parser.add_argument("--topic", default="events")
    args = parser.parse_args()
    setup_logging(args.node_id)
    bootstrap_servers = [s.strip() for s in args.bootstrap.split(",") if s.strip()]
    logging.info("Node-id=%s peers=%r topic=%s", args.node_id, args.peer, args.topic)
    node = Node(
         node_id=args.node_id,
         peers=args.peer,
         bootstrap_servers=bootstrap_servers,
         topic=args.topic,
    )

    try:
        await node.start()
    except Exception as e:
        logging.exception("Failed to start Node: %s", e)
        return  # <-- Kafka isn't running etc. exit here.

    # Example: send ping messages
    async def demo_sender() -> None:
        seq = 0
        while True:
            for peer in node.peers:
                await node.send(
                    to_node=peer,
                    msg_type="ping",
                    payload={"from": node.node_id, "seq": seq},
                )
            seq += 1
            await asyncio.sleep(5)

    if node.peers:
        asyncio.create_task(demo_sender())

    try:
        while True:
            await asyncio.sleep(3600)
    except KeyboardInterrupt:
        logging.info("Received ^C")
    finally:
        await node.stop()


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
