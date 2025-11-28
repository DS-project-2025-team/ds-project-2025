from collections import deque
from typing import Literal

from entities.leader_state import LeaderState
from entities.log_entry import LogEntry
from entities.raft_log import RaftLog
from roles.role import Role
from logger_service import logger
from message_service import MessageService


class Leader:
    def __init__(
        self,
        message_service: MessageService,
        log: RaftLog,
        queue: deque[int] | None = None,
    ) -> None:
        self.__message_service = message_service
        self.__queue: deque[int] = queue or deque()
        self.__log = log

    def run(self) -> Literal[Role.FOLLOWER]:
        logger.info("Changing role to FOLLOWER")
        return Role.FOLLOWER

    def __next_task(self) -> int | None:
        task = None

        while self.__queue:
            task = self.__queue.popleft()

            if not self.__log.completed_tasks[task]:
                self.__queue.append(task)
                break

        return task

    def __complete_task(self, task: int) -> None:
        entry = LogEntry(self.__log.term, lambda state: __complete_task(state, task))

        self.__log.append(entry)
        self.__log.commit()


def __complete_task(state: LeaderState, task: int) -> None:
    state.completed_tasks[task] = True
