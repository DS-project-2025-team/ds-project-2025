import logging
import sys

class LoggerService:
    def __init__(self) -> None:
        self._logger = logging.getLogger("ds-project-2025")
        if not self._logger.handlers:
            handler = logging.StreamHandler(sys.stdout) 
            formatter = logging.Formatter(
                "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            )
            handler.setFormatter(formatter)

            handler.setLevel(logging.DEBUG)
            self._logger.setLevel(logging.DEBUG)
            
            self._logger.addHandler(handler)

        self._logger.propagate = False

    def debug(self, msg: str, *args, **kwargs) -> None:
        self._logger.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args, **kwargs) -> None:
        self._logger.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs) -> None:
        self._logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs) -> None:
        self._logger.error(msg, *args, **kwargs)

    def exception(self, msg: str, *args, **kwargs) -> None:
        self._logger.exception(msg, *args, **kwargs)


logger = LoggerService()
