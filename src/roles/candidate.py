import asyncio
import random
from uuid import UUID

from entities.raft_log import RaftLog
from entities.server_address import ServerAddress
from logger_service import logger
from network.message_consumer import MessageConsumer
from network.message_consumer_factory import MessageConsumerFactory
from network.message_producer import MessageProducer
from network.topic import Topic
from roles.role import Role


class Candidate:
    def __init__(
        self,
        server: ServerAddress,
        peers: list[str],
        log: RaftLog,
        node_id: UUID,
    ) -> None:
        self.__peers = peers
        self.__log = log
        self.__id = node_id

        self.__producer = MessageProducer(server=server)
        self.__vote_consumer = MessageConsumer(Topic.VOTE, server=server)
        self.__heartbeat_consumer: MessageConsumer = (
            MessageConsumerFactory.heartbeat_consumer(server=server, node_id=node_id)
        )

    async def elect(self) -> Role:
        self.__log.term += 1
        current_term = self.__log.term
        logger.info(f"{self.__id} starting election for term {current_term}")

        votes_received = 1
        election_timeout = random.uniform(0.150, 0.300)
        total_votes_needed = (len(self.__peers) + 1) // 2 + 1

        request = {
            "term": current_term,
            "candidate_id": self.__id,
            "last_log_index": len(self.__log.entries) - 1,
            "last_log_term": self.__log.entries[-1].term if self.__log.entries else 0,
        }

        await self.__producer.send(Topic.VOTE_REQUEST, request)

        logger.info(f"{self.__id} sent vote requests to peers")

        while True:
            if self.__check_leader_existence():
                logger.info("Detected existing leader, reverting to FOLLOWER")
                return Role.FOLLOWER

            try:
                msg = await asyncio.wait_for(
                    self.__vote_consumer.receive(), timeout=election_timeout
                )
            except TimeoutError:
                logger.info(f"{self.__id} election timeout, restarting election")
                return Role.CANDIDATE

            if msg.get("type") == "vote" and msg.get("term") == current_term:
                if msg.get("vote_granted"):
                    votes_received += 1
                    logger.info(f"{self.__id} received vote from {msg.get('voter_id')}")

                    if votes_received > total_votes_needed:
                        logger.info(
                            f"{self.__id} won the election for term {current_term}"
                        )
                        return Role.LEADER

    async def __check_leader_existence(self) -> bool:
        try:
            await asyncio.wait_for(
                self.__heartbeat_consumer.receive(),
                timeout=1,
            )
            logger.info("Received heartbeat during election")

            return True

        except TimeoutError:
            return False
