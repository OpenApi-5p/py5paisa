"""
Uses loguru for formatting responses
TODO:
 - Add more extensive logging
"""

import sys
from loguru import logger

logger.remove()
logger.add(sys.stdout, level="INFO",
           format="<green>{time: HH:mm:ss}</green> | <bold>{message}</bold>")


def log_response(message: str) -> None:
    logger.info(message)
