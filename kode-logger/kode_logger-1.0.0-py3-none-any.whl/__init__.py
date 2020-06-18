import logging
import sys
from typing import List, Mapping, Optional, Callable, Dict

import kode_logger.formatters

name = 'kode_logger'


def create_json(
        context: str,
        *,
        tags: Optional[List[str]] = None,
        extra: Optional[Mapping] = None,
        tap: Optional[Callable[[Dict], Dict]] = None
) -> logging.Logger:
    logger = logging.getLogger(context)
    logger.propagate = False

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(kode_logger.formatters.JSONFormatter(tags=tags, extra=extra, tap=tap))

    logger.handlers = [handler]

    return logger
