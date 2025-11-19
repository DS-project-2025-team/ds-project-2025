from logging import Logger, getLogger


class LoggerService:
    def __init__(self, logger: Logger) -> None:
        self.__logger: Logger = logger

    def info(self, message: str) -> None:
        self.__logger.info(message)

    def error(self, message: str) -> None:
        self.__logger.error(message)

    def debug(self, message: str) -> None:
        self.__logger.debug(message)

    def warning(self, message: str) -> None:
        self.__logger.warning(message)


logger = LoggerService(getLogger(__name__))
