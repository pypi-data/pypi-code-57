"""logging
"""
import logging
from pathlib import Path

from dok8s.settings import LOG_DIR, LOG_LEVEL

LOGGER = logging.getLogger(__name__)
LOGGER_FORMAT = (
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
)


class CustomFormatter(logging.Formatter):
    """A custom logging formatter to add colors to logging levels."""

    grey = "\x1b[38;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = LOGGER_FORMAT

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        # pylint: disable=function-redefined
        log_format = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_format)
        return formatter.format(record)


def setup_logger(verbosity: int = 0) -> None:
    """Configure logger.

    Args:
        verbosity: Integer value for verbosity of logs (range from -1 to 2).

    Raises:
        NotADirectoryError: If given path directory is not valid.
    """
    if ~LOG_LEVEL:
        base_loglevel = getattr(logging, (~LOG_LEVEL).upper(), "WARNING")
        log_level = base_loglevel
    else:
        base_loglevel = getattr(logging, "WARNING")
        # Limit verbosity to value 2
        verbosity = min(verbosity, 2)
        log_level = base_loglevel - (verbosity * 10)
    LOGGER.setLevel(log_level)

    # If directory of logs exists, write to file.
    # Otherwise default to stream.
    log_dir = ~LOG_DIR
    if log_dir:
        output_dir = Path(log_dir)
        if not output_dir.is_dir():
            raise NotADirectoryError(f"{output_dir} is not a directory")
        filepath = output_dir / "dok8s.log"
        handler = logging.FileHandler(filepath)
        handler.setFormatter(logging.Formatter(LOGGER_FORMAT))
    else:
        handler = logging.StreamHandler()
        handler.setLevel(log_level)
        handler.setFormatter(CustomFormatter())

    LOGGER.addHandler(handler)
