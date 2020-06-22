import logging

LOG = None


def get_logger() -> logging.Logger:
    global LOG
    if not LOG:
        LOG = logging.getLogger('gs_config')
    return LOG
