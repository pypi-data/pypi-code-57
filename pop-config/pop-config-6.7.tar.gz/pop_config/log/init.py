"""
This sub is used to set up logging for pop projects and injects logging
options into conf making it easy to add robust logging
"""
# Import python libs
import logging


def __init__(hub):
    """
    Set up variables used by the log subsystem
    """
    logging.addLevelName(5, "TRACE")
    hub.log.LOGGER = {
        # Initialize the root logger
        "": logging.getLogger()
    }
    hub.log.LEVEL = {
        "notset": logging.NOTSET,
        "trace": 5,
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warn": logging.WARN,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "fatal": logging.FATAL,
        "critical": logging.CRITICAL,
    }

    # These should be overwritten by the integrated logger, but here's a contingency
    hub.log.INT_LEVEL = logging.INFO
    hub.log.log = hub.log.LOGGER[""].log
    hub.log.trace = lambda *args, **kwargs: hub.log.LOGGER[""].log(5, *args, **kwargs)
    hub.log.debug = hub.log.LOGGER[""].debug
    hub.log.info = hub.log.LOGGER[""].info
    hub.log.critical = hub.log.LOGGER[""].critical
    hub.log.warning = hub.log.LOGGER[""].warning
    hub.log.error = hub.log.LOGGER[""].error
