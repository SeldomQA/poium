import sys

from loguru import logger


class Logger:

    def __init__(self, level: str = "DEBUG", colorlog: bool = True):
        self.logger = logger
        self._colorlog = colorlog
        self._console_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</> {file} <level>| {thread.name} | {level} | {message}</level>"
        self._level = level
        self.set_level(self._colorlog, self._console_format, self._level)

    def set_level(self, colorlog: bool = True, format: str = None, level: str = "DEBUG"):
        if format is None:
            format = self._console_format
        try:
            from seldom.running.config import BrowserConfig
            from seldom import Seldom
            if Seldom.driver is not None:
                logfile = BrowserConfig.LOG_PATH
                _file_format = " {time:YYYY-MM-DD HH:mm:ss} | {file: <10} | {thread.name} | {level: <8} | {message}"
                logger.remove()
                logger.add(sys.stderr, level=level, colorize=colorlog, format=format)
                logger.add(logfile, level=level, colorize=colorlog, format=_file_format, encoding="utf-8")
        except ImportError:
            logger.remove()
            logger.add(sys.stderr, level=level, colorize=colorlog, format=format)

    def trace(self, msg: str):
        """
        trace log
        :param msg:
        :return:
        """
        return self.logger.trace(msg)

    def debug(self, msg: str):
        """
        debug log
        :param msg:
        :return:
        """
        return self.logger.debug(msg)

    def info(self, msg: str):
        """
        info log
        :param msg:
        :return:
        """
        self.logger.info(msg)

    def success(self, msg: str):
        """
        success log
        :param msg:
        :return:
        """
        return self.logger.success(msg)

    def warning(self, msg: str):
        """
        warning log
        :param msg:
        :return:
        """
        return self.logger.warning(msg)

    def error(self, msg: str):
        """
        error log
        :param msg:
        :return:
        """
        return self.logger.error(msg)

    def critical(self, msg: str):
        """
        critical log
        :param msg:
        :return:
        """
        return self.logger.critical(msg)


# log level: TRACE < DEBUG < INFO < SUCCESS < WARNING < ERROR
logging = Logger(level="TRACE")
