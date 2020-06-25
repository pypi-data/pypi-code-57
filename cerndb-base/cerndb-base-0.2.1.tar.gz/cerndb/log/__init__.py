"""Module with Basic logging configuration for IT-DB Python modules."""
import logging
from cerndb.config import CFG


class CerndbLoggerException(Exception):
    """Raised when the logger couldn't be initialized."""


def setup_root_logger(config=None, tag: str = None):
    """Prepare a root logger.

    You can either use

    CerndbLoggerExceptionRaises:
        CerndbLoggerException:
            - when log_level or log_file are not defined in the config file.
            - when log_level has been incorrectly defined (not one of DEBUG,
                    INFO, WARNING, ERROR, CRITICAL)
    """

    # Auto-reinitialize the logger if --debug provided
    config.register_on_change(setup_root_logger)

    # These values are used if the config file is missing them
    # or not readable

    defaults = {
        "level": "INFO",
        "file": "/var/log/cerndb.log",
        "fmt": "%(asctime)s [%(module)s:%(lineno)d][%(process)s] " +
               "%(levelname)s {0} %(message)s",
        "datefmt": '%Y-%m-%dT%H:%M:%S%z'
    }

    # Fallback to defaults if the values are not in the config file
    try:
        log_conf = config["log"]
    except KeyError:
        # log key not defined in the config file
        log_conf = defaults

    log_level = log_conf.get("level", defaults["level"])
    log_file = log_conf.get("file", defaults["file"])
    log_datefmt = log_conf.get("datefmt", defaults["datefmt"])

    # Prioritize a tag provided via arguments over configuration file and
    # default values
    config_tag = log_conf.get("tag", "CERNDB")
    if tag:
        log_tag = tag
    else:
        log_tag = config_tag

    log_fmt = log_conf.get("fmt", defaults["fmt"]).format(log_tag)

    if log_level not in ["INFO", "ERROR", "WARNING", "CRITICAL", "DEBUG"]:
        raise CerndbLoggerException(
            f"Incorrect level '{log_level}' in the config "
            "file {config.used_file}.")

    root_logger = logging.getLogger()
    # To prevent double messages if before importing logging.* was used
    # by default then - basicConfig is run and it adds handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    root_logger.setLevel(log_level)

    formatter = logging.Formatter(log_fmt, log_datefmt)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)


def get_logger(tag: str):
    """Return logger object with default configuration and custom tag"""
    setup_root_logger(config=CFG, tag=tag)
    return logging.getLogger()


setup_root_logger(config=CFG)
logger = logging.getLogger()
