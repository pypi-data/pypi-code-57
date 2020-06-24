import logging

log = logging.getLogger(__name__)


class Strategy:
    """ Holds the trading algorithm. A strategy consumes data feeds
    and returns trading orders.

    Args:
        name: the name of the strategy
    """

    def __init__(self, name: str):

        log.info(f"Initiating Strategy. name={name}")
        self.name = name
