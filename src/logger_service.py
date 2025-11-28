from loguru import logger as _logger


class LoggerService:
    def __init__(self) -> None:
        self.__logger = _logger.opt(depth=1, colors=True)

    def info(self, message: str) -> None:
        self.__logger.info(message)

    def error(self, message: str) -> None:
        self.__logger.error(message)

    def debug(self, message: str) -> None:
        self.__logger.debug(message)

    def warning(self, message: str) -> None:
        self.__logger.warning(message)


logger = LoggerService()
