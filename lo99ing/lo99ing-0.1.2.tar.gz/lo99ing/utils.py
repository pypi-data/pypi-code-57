"""
Utilities to make lo99ing friendly.
"""

import logging
import os
import types
import time
import datetime
from pathlib import Path

from .logger import Lo99er
from .handlers import enable_stderr, disable_stderr, enable_file
from .level import set_log_level, log_level_manager, to_level
from .formatter import formatter as _formatter
from .misc import logging_lock


################################################################################
# logger getter

def get_logger(name, level=None, propagate=True):
    """
    Finds a logger.  If the logger doesn't already exist, will initialize it appropriately:
    Will resolve an initial log level, and update log_level_manager.
    Will enable logging to stderr if propagate=False.
    """

    name = _name_fixup(name)
    if level is not None:
        level = to_level(level)

    # find the actual logger
    logger = logging.getLogger(name)

    with logging_lock:

        is_initialized = log_level_manager.has_initial(name)
        is_lo99er = isinstance(logger, Lo99er)
        cur_level = logger.level

        # initialize it if needed
        if not is_initialized:
            if is_lo99er:
                if level is not None:
                    # a new Lo99er. caller passed a specific level. we use it.
                    initial_level = level
                else:
                    # a new Lo99er. using its default level
                    initial_level = cur_level
            else:
                # the logger was created before importing lo99ing
                if cur_level == logging.NOTSET:
                    # a Logger with no level set. use the level passed by the caller (if any)
                    # NOTE this should never happen before all loggers created before importing
                    # lo99ing get their level in _bootstrap, and all logger created after get their
                    # level in Lo99er.__init__()
                    initial_level = level
                else:
                    # a Logger with level already set. ignore level passed by the caller (if any)
                    initial_level = cur_level

            if initial_level is not None:
                log_level_manager.set_initial(name, initial_level)
                # effective level can be different than level if set_log_level_override(name, ...)
                # is called before first call to get_logger(name, ...)
                effective_level = log_level_manager.get_effective(name)
                set_log_level(name, effective_level)

            logger.propagate = propagate
            if not propagate:
                # this logger is root-like -- set default handlers:
                enable_stderr(logger)

    return logger


def get_file_logger(name, filename, level=None, rotate=False, **kwargs):
    """
    Create an "independent" logger which writes to a file only.
    If rotate=True, will create a daily-rotating logger (filename should contain '*',
    which is replaced with the date).
    """
    logger = get_logger(name, level, propagate=False)
    disable_stderr(logger)
    enable_file(filename, logger=logger, rotate=rotate, **kwargs)
    return logger


def _name_fixup(name):
    """
    >>> _name_fixup('foo.bar')
    'foo.bar'
    >>> _name_fixup('/usr/lib/python3.5/abc.py')
    'abc'
    >>> _name_fixup('/usr/lib/python3.5/distutils/__init__.py')
    'distutils'
    """
    if os.path.sep in name:
        # used with filename, like: get_logger(__file__)
        p = Path(name)
        res = os.path.splitext(p.name)[0]
        if res in ('', '__init__'):
            res = p.parent.name
        return res
    else:
        return name


################################################################################
# clock

def use_utc(formatter=None):
    """
    Log messages to display timestamps in UTC.
    """
    if formatter is None:
        formatter = _formatter
    formatter.converter = time.gmtime


def use_clock(clock, formatter=None):
    """
    Use a custom clock for creating log-message timestamps.
    :param clock: a callable which takes no args and returns a ``datetime.datetime`` object.
    """
    if formatter is None:
        formatter = _formatter

    originalFormatTime = formatter.formatTime

    def _formatTime(self, record, datefmt=None):
        ct = _logging_timestamp(record.created)
        if not isinstance(ct, datetime.datetime):
            return originalFormatTime(record, datefmt)

        # we need to override this method to ensure the millis are taken from the converted
        # creation time, and not from the record (which would be the case if we just changed
        # formatter.converter to be _logging_timestamp.
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            s = ct.strftime("%Y-%m-%d %H:%M:%S")
            s = '%s,%03d' % (s, ct.microsecond / 1000)
        return s

    def _logging_timestamp(record_created):
        now = clock()
        if now is not None:
            return now
        if record_created is not None:
            return record_created
        return datetime.datetime.utcnow()

    if formatter is None:
        formatter = _formatter
    formatter.formatTime = types.MethodType(_formatTime, formatter)


################################################################################
