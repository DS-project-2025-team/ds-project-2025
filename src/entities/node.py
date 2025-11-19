from roles.role import Role
from services.message_service import (
    MessageService,
)
from services.message_service import (
    message_service as default_message_service,
)


class Node:
    def __init__(
        self,
        role: Role = Role.FOLLOWER,
        message_service: MessageService = default_message_service,
    ) -> None:
        self.__role: Role = role
        self.__message_service: MessageService = message_service
