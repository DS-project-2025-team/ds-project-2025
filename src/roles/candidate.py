import asyncio
from uuid import UUID

from entities.raft_log import RaftLog
from entities.second import Second
from entities.server_address import ServerAddress
from logger_service import logger
from network.message_consumer import MessageConsumer
from network.message_consumer_factory import MessageConsumerFactory
from network.message_producer import MessageProducer
from network.topic import Topic
from roles.role import Role
from utils.async_loop import async_loop


class Candidate:
    def __init__(
        self,
        server: ServerAddress,
        peers: list[str],
        log: RaftLog,
        node_id: UUID,
        vote_timeout: Second = Second(20),
    ) -> None:
        self.__peers = peers
        self.__log = log
        self.__id = node_id
        self.__vote_timeout = vote_timeout

        self.__producer = MessageProducer(server=server)
        self.__vote_consumer = MessageConsumerFactory.vote_consumer(
            server=server, node_id=node_id
        )
        self.__heartbeat_consumer: MessageConsumer = (
            MessageConsumerFactory.heartbeat_consumer(server=server, node_id=node_id)
        )

    async def elect(self) -> Role:
        self.__log.term += 1
        current_term = self.__log.term
        logger.info(f"{self.__id} starting election for term {current_term}")

        begin_time = asyncio.get_event_loop().time()
        role = Role.FOLLOWER

        votes_received = 1
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
                break

            votes_received += await self.__receive_vote(current_term)

            if votes_received >= total_votes_needed:
                role = Role.LEADER
                logger.info(f"{self.__id} won the election for term {current_term}")

                break

            try:
                await self.__check_timeout(begin_time)
                logger.info("Election timed out")
            except TimeoutError:
                return Role.CANDIDATE

        return role

    async def __receive_vote(self, current_term: int, timeout: float = 0.5) -> int:
        try:
            vote = await self.__vote_consumer.receive(Second(timeout))
        except TimeoutError:
            return 0

        logger.debug("Received a vote: %r", vote)
        if vote["term"] != current_term and vote["recipient_id"] != self.__id:
            return 0

        logger.info("Received a vote")
        return 1

    @async_loop
    async def __check_timeout(self, begin_time: float) -> None:
        if asyncio.get_event_loop().time() - begin_time > self.__vote_timeout:
            raise TimeoutError()

    async def __check_leader_existence(self) -> bool:
        try:
            await self.__heartbeat_consumer.receive(timeout=Second(1))

            logger.info("Received heartbeat during election")

            return True

        except TimeoutError:
            return False
