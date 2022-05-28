import io
import sys
from loguru import logger


log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</> {file} <level>| {level} | {message}</level>"
logger.remove()
sys.stderr = io.StringIO()
# print to consoles
logger.add(sys.stdout, level="DEBUG", colorize=True, format=log_format)
# print to HTML report
logger.add(sys.stderr, level="DEBUG", colorize=False, format=log_format)


logging = logger
