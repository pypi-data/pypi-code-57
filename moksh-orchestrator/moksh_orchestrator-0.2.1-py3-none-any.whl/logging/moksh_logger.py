from enum import Enum
from functools import wraps
import time
import logging
import sys

def INFO():
    logging.basicConfig(filename='{}.log'.format(__file__.split('/')[-1:][0].split('.py')[0]), level=logging.INFO)


def ERROR():
    logging.basicConfig(filename='{}.log'.format(__file__.split('/')[-1:][0].split('.py')[0]), level=logging.ERROR)


def WARNING():
    logging.basicConfig(filename='{}.log'.format(__file__.split('/')[-1:][0].split('.py')[0]),
                        level=logging.WARNING)


def DEBUG():
    logging.basicConfig(filename='{}.log'.format(__file__.split('/')[-1:][0].split('.py')[0]), level=logging.DEBUG)


class LoggingLevel(Enum):
    INFO = INFO
    ERROR = ERROR
    WARNING = WARNING
    DEBUG = DEBUG


def moksh_logger(original_function):
    MokshLogger.moksh_log_debug(original_function.__name__)

    @wraps(original_function)
    def wrapper_function(*args, **kwargs):
        logging.info('{} Ran with args: {} & kwargs {}'.format(original_function.__name__, args, kwargs))
        return original_function(*args, **kwargs)

    return wrapper_function


def moksh_timer(original_function):
    @wraps(original_function)
    def wrapper(*args, **kwargs):
        t1 = time.time()
        return_value = original_function(*args, **kwargs)
        t2 = time.time() - t1
        MokshLogger.moksh_log_debug('{} ran in: {} seconds'.format(original_function.__name__, t2))
        return return_value

    return wrapper


class MokshLogger:

    @staticmethod
    def configure_logger(logging_level: LoggingLevel):
        logger_level_setting_function = logging_level

        logger_level_setting_function()

        logging.basicConfig(filename='{}.log'.format(__file__.split('/')[-1:][0].split('.py')[0]), level=logging.INFO)
        rootLogger = logging.getLogger()
        loggingHandler = logging.StreamHandler(sys.stdout)
        loggingHandler.setFormatter(logging.Formatter("%(asctime)s %(threadName)-12s] [%(levelname)-5s]  %(message)s"))
        rootLogger.addHandler(loggingHandler)

    @staticmethod
    def moksh_log_debug(message):
        logging.debug(message)

    @staticmethod
    def moksh_log_error(message):
        logging.error(message)

    @staticmethod
    def moksh_log_warning(message):
        logging.warning(message)

    @staticmethod
    def moksh_log_info(message):
        logging.info(message)
