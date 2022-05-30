import sys
import time
from loguru import logger
from poium import config


class Logger:

    def __init__(self, level: str = "DEBUG", colorlog: bool = True):
        self.logger = logger
        self._colorlog = colorlog
        self._console_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</> {file} <level>| {level} | {message}</level>"
        self._level = level
        self.set_level(self._colorlog, self._console_format, self._level)

    def set_level(self, colorlog: bool = True, format: str = None, level: str = "DEBUG"):
        if format is None:
            format = self._console_format
        logger.remove()
        logger.add(sys.stderr, level=level, colorize=colorlog, format=format)

    def trace(self, msg: str):
        if config.printLog is True:
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{now} | TRACE | {str(msg)}")
        return self.logger.trace(msg)

    def debug(self, msg: str):
        if config.printLog is True:
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{now} | DEBUG | {str(msg)}")
        return self.logger.debug(msg)

    def info(self, msg: str):
        if config.printLog is True:
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{now} | INFO | {str(msg)}")
        return self.logger.info(msg)

    def success(self, msg: str):
        if config.printLog is True:
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{now} | SUCCESS | {str(msg)}")
        return self.logger.success(msg)

    def warning(self, msg: str):
        if config.printLog is True:
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{now} | WARNING | {str(msg)}")
        return self.logger.warning(msg)

    def error(self, msg: str):
        if config.printLog is True:
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{now} | ERROR | {str(msg)}")
        return self.logger.error(msg)

    def critical(self, msg: str):
        if config.printLog is True:
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{now} | CRITICAL | {str(msg)}")
        return self.logger.critical(msg)

    def printf(self, msg: str):
        return self.logger.success(msg)


# log level: TRACE < DEBUG < INFO < SUCCESS < WARNING < ERROR
logging = Logger(level="TRACE")
