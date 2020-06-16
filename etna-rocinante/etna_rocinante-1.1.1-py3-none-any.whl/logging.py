import logging
from panza.jobs import add_logger_handler
from typing import Iterable


def init_logging(handlers: Iterable, debug: bool = False) -> logging.Logger:
    """
    Initialize logging for rocinante

    :param handlers:            the handlers to setup for logging
    :param debug:               whether debug output should be logged (default is False)
    :return:                    the initialized logger
    """

    logger = logging.getLogger("rocinante")
    logger.setLevel(logging.DEBUG if debug is True else logging.INFO)
    formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s')

    for handler in handlers:
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        add_logger_handler(handler)

    return logger
