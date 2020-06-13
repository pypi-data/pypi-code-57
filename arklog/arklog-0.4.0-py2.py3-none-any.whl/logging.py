import logging
import pathlib
import types
from functools import wraps, partial
from typing import Callable

import yaml

CRITICAL = logging.CRITICAL
ERROR = logging.ERROR
WARNING = logging.WARNING
SUCCESS = 21
INFO = logging.INFO
EXTRA = 11
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET


class ColorFormatter(logging.Formatter):
    """Formatter supporting colors."""
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    ORANGE = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHTGRAY = "\033[0;37m"
    DARKGRAY = "\033[1;30m"
    LIGHTRED = "\033[1;31m"
    LIGHTGREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHTBLUE = "\033[1;34m"
    LIGHTPURPLE = "\033[1;35m"
    LIGHTCYAN = "\033[1;36m"
    WHITE = "\033[1;37m"
    NC = "\033[0m"

    COLORS = {
        DEBUG: BLUE,
        EXTRA: LIGHTPURPLE,
        INFO: WHITE,
        SUCCESS: GREEN,
        WARNING: YELLOW,
        ERROR: LIGHTRED,
        CRITICAL: RED,
    }

    def format(self, record) -> str:
        """Same as logging.Formatter except it now adds color."""
        color = self.COLORS[record.levelno]
        return f"{color}{logging.Formatter.format(self, record)}{self.NC}"


def add_logger_methods() -> None:
    """Patch in two methods for the Python logger."""
    logging.Logger.success = types.MethodType(success_wrap, logging.Logger)
    logging.RootLogger.success = types.MethodType(success_wrap, logging.RootLogger)
    logging.Logger.extra = types.MethodType(extra_wrap, logging.Logger)
    logging.RootLogger.extra = types.MethodType(extra_wrap, logging.RootLogger)


def create_logger(name: str, level: int = logging.DEBUG, file_path: pathlib.Path = None) -> logging.Logger:
    """
    Create logger instance.
    The logger will output to stdout if no file_path is provided.
    """
    add_logger_methods()

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.success = types.MethodType(success_wrap, logger)
    logger.extra = types.MethodType(extra_wrap, logger)
    formatter = ColorFormatter(fmt="%(message)s")

    # Don't add colors when logging to a file because they will not be displayed
    if file_path:
        file_handler = logging.FileHandler(f"{file_path}")
        logger.addHandler(file_handler)
    else:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


def set_defaults(level: int = logging.DEBUG, file_path: [pathlib.Path, str] = None) -> None:
    """Set the default logger options."""
    add_logger_methods()

    if file_path:
        logging.basicConfig(
            filename=f"{file_path}",
            level=level,
            format="[%(asctime)s] %(levelname)s - %(message)s",
            datefmt="%H:%M:%S",
        )
    else:
        formatter = ColorFormatter(fmt="%(message)s")
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logging.basicConfig(
            level=level,
            format="[%(asctime)s] %(levelname)s - %(message)s",
            datefmt="%H:%M:%S",
            # handlers=[console_handler],
        )


def success_wrap(self, msg, *args, **kwargs):
    """"""
    if self.isEnabledFor(SUCCESS):
        self._log(SUCCESS, msg, args, **kwargs)


def success(msg, *args, **kwargs):
    """"""
    if len(logging.root.handlers) == 0:
        set_defaults()
    try:
        logging.root.success(msg, *args, **kwargs)
    except (AttributeError, TypeError):
        logging.root.success = types.MethodType(success_wrap, logging.root)
        logging.root.success(msg, *args, **kwargs)


def extra_wrap(self, msg, *args, **kwargs):
    """"""
    if self.isEnabledFor(EXTRA):
        self._log(EXTRA, msg, args, **kwargs)


def extra(msg, *args, **kwargs):
    """"""
    if len(logging.root.handlers) == 0:
        set_defaults()
    try:
        logging.root.extra(msg, *args, **kwargs)
    except (AttributeError, TypeError):
        logging.root.extra = types.MethodType(extra_wrap, logging.root)
        logging.root.extra(msg, *args, **kwargs)


def set_from_file(file_path: pathlib.Path):
    """"""
    with file_path.open("rt") as f:
        config_data = yaml.safe_load(f.read())
        logging.config.dictConfig(config_data)


def attach_wrapper(obj, func=None):
    if func is None:
        return partial(attach_wrapper, obj)
    setattr(obj, func.__name__, func)
    return func


def log(level: int, message: str) -> Callable:
    """Decorator to log."""

    def decorate(func: Callable) -> Callable:
        logger = logging.getLogger(func.__module__)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        log_message = f"{func.__name__} - {message}"

        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.log(level, log_message)
            return func(*args, **kwargs)

        @attach_wrapper(wrapper)
        def set_level(new_level):
            nonlocal level
            level = new_level

        @attach_wrapper(wrapper)
        def set_message(new_message):
            nonlocal log_message
            log_message = f"{func.__name__} - {new_message}"

        return wrapper

    return decorate
