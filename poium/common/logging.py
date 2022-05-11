import sys
import time
import platform
import logging.handlers
from colorama import Fore, Style

_logger = logging.getLogger('poium')
_logger.setLevel(logging.DEBUG)
_handler = logging.StreamHandler(sys.stdout)
_handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
_logger.addHandler(_handler)
# _logger.removeHandler(_handler)

colorLog = True


def debug(msg):
    _logger.debug("DEBUG " + str(msg))


def info(msg):
    if colorLog is True:
        _logger.info(Fore.GREEN + " [INFO] " + str(msg) + Style.RESET_ALL)
    else:
        msg = msg.encode('gbk', 'ignore').decode('gbk', "ignore")
        _logger.info("[INFO] " + str(msg))


def error(msg):
    if colorLog is True:
        _logger.error(Fore.RED + " [ERROR] " + str(msg) + Style.RESET_ALL)
    else:
        msg = msg.encode('gbk', 'ignore').decode('gbk', "ignore")
        _logger.error("[ERROR] " + str(msg))


def warn(msg):
    if colorLog is True:
        _logger.warning(Fore.YELLOW + " [WARNING] " + str(msg) + Style.RESET_ALL)
    else:
        msg = msg.encode('gbk', 'ignore').decode('gbk', "ignore")
        _logger.warning("[WARNING] " + str(msg))


def printf(msg):
    if colorLog is True:
        _logger.info(Fore.CYAN + " [PRINT] " + str(msg) + Style.RESET_ALL)
    else:
        msg = msg.encode('gbk', 'ignore').decode('gbk', "ignore")
        _logger.info("[PRINT] " + str(msg))


def set_level(level):
    """ 设置log级别

    :param level: logging.DEBUG, logging.INFO, logging.WARN, logging.ERROR
    :return:
    """
    _logger.setLevel(level)


def set_level_to_debug():
    _logger.setLevel(logging.DEBUG)


def set_level_to_info():
    _logger.setLevel(logging.INFO)


def set_level_to_warn():
    _logger.setLevel(logging.WARN)


def set_level_to_error():
    _logger.setLevel(logging.ERROR)
