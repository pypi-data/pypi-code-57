import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from pythonjsonlogger import jsonlogger  # noqa: I900


def _setup_logging(where_level):
    logger = logging.getLogger(__name__)

    json_format = jsonlogger.JsonFormatter(
        '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        json_indent=2
    )

    switcher = {
        "error": logging.ERROR,
        "warn": logging.WARNING,
        "debug": logging.DEBUG,
        "info": logging.INFO
    }

    to, _, level = str(where_level).partition(":")
    chosen_level = switcher.get(level.lower(), logging.DEBUG)
    logger.setLevel(chosen_level)

    if to == "stdout":
        s_handler = logging.StreamHandler(stream=sys.stdout)
        s_handler.setLevel(chosen_level)
        logger.addHandler(s_handler)
    else:
        logging.StreamHandler(stream=None)

    log_folder = "logs/"
    Path(log_folder).mkdir(parents=True, exist_ok=True)

    r_handler = RotatingFileHandler(
        f'{log_folder}sdk.log', mode='w', backupCount=3)
    r_handler.setLevel(logging.DEBUG)
    r_handler.setFormatter(json_format)
    logger.addHandler(r_handler)

    return logger
