from contextlib import AbstractAsyncContextManager


class PingService(AbstractAsyncContextManager):
    """
    Class for counting alive consumers, assuming one consumer per group.
    """

    def __init__(self) -> None:
        pass
