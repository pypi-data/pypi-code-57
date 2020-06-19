import sys
import logging


class LoggingMixin:
    # CRITICAL 50
    # ERROR 40
    # WARNING 30
    # INFO 20
    # DEBUG 10
    # NOTSET 0
    LOGGING_LEVEL: int = 10

    LOGGING_FORMAT: str = '[%(asctime)s] {%(name)s:%(lineno)d} %(levelname)s - %(message)s'

    def initialize_logging(self):
        """
        Initialize basic logging to stdout
        """
        logging.basicConfig(
            stream=sys.stdout,
            level=self.LOGGING_LEVEL,
            format=self.LOGGING_FORMAT
        )
