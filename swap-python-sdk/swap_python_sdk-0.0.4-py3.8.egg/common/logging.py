import logging
import sys
from swap.common.config import Settings

log_level = logging.getLevelName(Settings.LOG_LEVEL)

log_handler = logging.StreamHandler(sys.stdout)

logger = logging.getLogger()

logger.addHandler(log_handler)

logger.setLevel(log_level)
