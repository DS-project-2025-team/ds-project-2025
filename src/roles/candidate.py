import asyncio
import random
from typing import Literal

from entities.raft_log import RaftLog
from logger_service import logger
from network.message_service import MessageService
from roles.role import Role


class Candidate:
    def __init__(
        self, message_service: MessageService, peers: list[str], log: RaftLog
    ) -> None:
        self.__message_service = message_service
        self.__peers = peers
        self.__log = log

    async def elect(self) -> Literal[Role.LEADER, Role.CANDIDATE]:
        self.__log.term += 1
        current_term = self.__log.term
        logger.info(f"{self.__log.node_id} starting election for term {current_term}")

        votes_received = 1
        election_timeout = random.uniform(0.150, 0.300)
        total_votes_needed = (len(self.__peers) + 1) // 2 + 1

        request = {
            "type": "request_vote",
            "term": current_term,
            "candidate_id": self.__log.node_id,
            "last_log_index": len(self.__log.entries) - 1,
            "last_log_term": self.__log.entries[-1].term if self.__log.entries else 0,
        }

        for peer in self.__peers:
            await self.__message_service.send(peer, request)

        logger.info(f"{self.__log.node_id} sent vote requests to peers")

        try:
            while True:
                msg = await asyncio.wait_for(
                    self.__message_service.receive(), timeout=election_timeout
                )

                if msg.get("type") == "heartbeat":
                    logger.info(f"{self.__log.node_id} received heartbeat from leader")
                    return Role.FOLLOWER

                if msg.get("type") == "vote" and msg.get("term") == current_term:
                    if msg.get("vote_granted"):
                        votes_received += 1
                        logger.info(
                            f"{self.__log.node_id} received vote from {msg.get('voter_id')}"
                        )

                        if votes_received > total_votes_needed:
                            logger.info(
                                f"{self.__log.node_id} won the election for term {current_term}"
                            )
                            return Role.LEADER

        except TimeoutError:
            logger.info(f"{self.__log.node_id} election timeout, restarting election")
            return Role.CANDIDATE
