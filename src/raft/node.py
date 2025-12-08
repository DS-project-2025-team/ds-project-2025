from asyncio import TaskGroup
from contextlib import AbstractAsyncContextManager
from types import TracebackType
from typing import Self
from uuid import UUID, uuid4

from entities.server_address import ServerAddress
from network.message_consumer import MessageConsumer
from network.message_consumer_factory import MessageConsumerFactory
from network.message_producer import MessageProducer
from network.topic import Topic
from raft.entities.log import Log
from raft.roles.follower import Follower
from raft.roles.leader import Leader
from raft.roles.role import Role
from raft.vote_receiver_service import VoteReceiverService
from services.logger_service import logger
from utils.async_loop import async_loop


class Node(AbstractAsyncContextManager):
    def __init__(
        self,
        server: ServerAddress,
        node_id: UUID | None = None,
        role: Role = Role.FOLLOWER,
        log: Log | None = None,
    ) -> None:
        self.node_id: UUID = node_id or uuid4()
        self.__server: ServerAddress = server
        self.__role: Role = role
        self.__log: Log = log or Log()

        self.__producer: MessageProducer = MessageProducer(server=server)
        self.__ping_consumer: MessageConsumer = MessageConsumerFactory.ping_consumer(
            server=server, node_id=self.node_id
        )
        self.__vote_receiver: VoteReceiverService = VoteReceiverService(
            server=server,
            node_id=self.node_id,
            producer=self.__producer,
            log=self.__log,
        )

    async def __aenter__(self) -> Self:
        await self.__producer.__aenter__()
        await self.__ping_consumer.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.__producer.__aexit__(exc_type, exc_value, traceback)
        await self.__ping_consumer.__aexit__(exc_type, exc_value, traceback)

    @async_loop
    async def run(self) -> None:
        async with TaskGroup() as group:
            _task1 = group.create_task(self.__run_raft())
            _task2 = group.create_task(self.__handle_ping())
            _task3 = group.create_task(self.__vote_receiver.handle_vote())

    @async_loop
    async def __run_raft(self) -> None:
        match self.__role:
            case Role.FOLLOWER:
                async with Follower(
                    server=self.__server,
                    node_id=self.node_id,
                    producer=self.__producer,
                ) as follower:
                    self.__role = await follower.run()

            case Role.CANDIDATE:
                # candidate = Candidate(self.__message_service, self.peers, self.__log)
                # self.__role = await candidate.elect()
                self.__role = Role.LEADER

            case Role.LEADER:
                async with Leader(
                    log=self.__log,
                    server=self.__server,
                    node_id=self.node_id,
                    producer=self.__producer,
                ) as leader:
                    self.__role = await leader.run()

    @async_loop
    async def __handle_ping(self) -> None:
        message = await self.__ping_consumer.receive()
        sender = message.data["sender"]

        logger.debug(f"Received ping from {sender}")

        payload = {
            "receiver": sender,
        }

        await self.__producer.send(Topic.PING_RESPONSE, payload)
