import logging
import sys
from collections.abc import Callable

LogFunc = Callable[..., None]


class LoggerService:
    def __init__(self) -> None:
        self._logger = logging.getLogger("ds-project-2025")
        if not self._logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            )
            handler.setFormatter(formatter)

            handler.setLevel(logging.INFO)
            self._logger.setLevel(logging.INFO)

            self._logger.addHandler(handler)

    def set_level(self, level: int) -> None:
        """Set logger and handlers to given level."""
        self._logger.setLevel(level)
        for handler in self._logger.handlers:
            handler.setLevel(level)

    def get_level(self) -> int:
        return self._logger.getEffectiveLevel()

    def debug(self, msg: str, *args: object) -> None:
        self._logger.debug(msg, *args)

    def info(self, msg: str, *args: object) -> None:
        self._logger.info(msg, *args)

    def warning(self, msg: str, *args: object) -> None:
        self._logger.warning(msg, *args)

    def error(self, msg: str, *args: object) -> None:
        self._logger.error(msg, *args)

    def exception(self, msg: str, *args: object) -> None:
        self._logger.exception(msg, *args)


logger = LoggerService()
