import sys
import warnings

from loguru import logger as log

warnings.filterwarnings("ignore")

logger = log

logger.remove()

logger.add(
    sys.stderr,
    format="<green>{time:DD-MM-YYYY at HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>",
    level="DEBUG",
    colorize=True,
    enqueue=True,
)
