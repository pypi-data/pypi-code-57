"""
Definition of logger handlers, and tools for manipulating logger handlers.
"""

import logging
import logging.handlers
import sys
import time
import datetime
import traceback

from .formatter import formatter


################################################################################

class _ErrorHandlerMixin:
    """
    A mixin to improve error handling.
    The improved error handler prints the location (file, line num) of the logging call
    which failed.
    """

    def handleError(self, record):
        if not logging.raiseExceptions:
            return

        output_stream = getattr(self, 'stream')
        if not output_stream:
            output_stream = sys.stderr
        try:
            ei = sys.exc_info()
            traceback.print_exception(ei[0], ei[1], ei[2], None, output_stream)
            output_stream.write('Logged from %s:%s\n' % (record.pathname, record.lineno))
            # NOTE: if output stream is self.stream, the output might be buffered, but we avoid
            # flushing for threadsafety
        except (AttributeError, IOError):
            pass


class StreamHandler(_ErrorHandlerMixin, logging.StreamHandler):
    """
    Same as ``logging.StreamHandler``, but with an improved error-handler.
    """
    pass


class FileHandler(_ErrorHandlerMixin, logging.FileHandler):
    """
    Same as ``logging.FileHandler``, but with an improved error-handler.
    """
    pass


class DailyRotatingFileHandler(_ErrorHandlerMixin, logging.handlers.TimedRotatingFileHandler):
    """
    A customized daily TimedRotatingFileHandler.

    The class takes a filename_pattern, which is a path containing a '*' date-placeholder,
    which is replaced with the appropriate date, in YYYYMMDD format.

    This class always uses: when='MIDNIGHT', backupCount=0, utc=True, atTime=None.
    Since utc=True, it doesn't hanlde DST changes.

    """

    DATE_FORMAT = '%Y%m%d'

    def __init__(self, filename_pattern, **kwargs):
        """
        :param filename_pattern: a path (str or Path), with a single '*' date-placeholder
        """
        if filename_pattern:
            filename_pattern = str(filename_pattern)  # support Path
        fptn = filename_pattern
        filename_pattern = filename_pattern.replace('*', self.DATE_FORMAT)
        if fptn == filename_pattern:
            raise ValueError('filename_pattern must contain "*"', filename_pattern)
        self.filename_pattern = filename_pattern
        for k in ['when', 'utc', 'backupCount', 'atTime']:
            if k in kwargs:
                raise TypeError('arg not supported', k)
        first_filename = self.get_filename_for_time(self.now())
        logging.handlers.TimedRotatingFileHandler.__init__(
            self, first_filename, when='MIDNIGHT', utc=True, **kwargs)

        # making sure super doesn't use these, because we don't want it to.
        self.suffix = None
        self.extMatch = None

    def doRollover(self):

        # close current file
        if self.stream:
            self.stream.close()
            self.stream = None

        # write to a new file
        self.baseFilename = self.get_filename_for_time(self.now())
        self.mode = 'a'
        self.stream = self._open()

        # compute next
        currentTime = int(time.time())
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        self.rolloverAt = newRolloverAt

    def now(self):
        return datetime.datetime.utcnow()

    def get_filename_for_time(self, dt):
        return dt.strftime(self.filename_pattern)


################################################################################
# globals

stderr_handler = StreamHandler(sys.stderr)
stderr_handler.setFormatter(formatter)


################################################################################
# add/remove handlers

def enable_stderr(logger=None):
    """ Adds a stderr StreamHandler to root logger (if not already there). """
    if logger is None:
        logger = logging.root

    # Don't add if it already has one
    if any(_is_stderr_handler(h) for h in logger.handlers):
            return

    logger.addHandler(stderr_handler)


def disable_stderr(logger=None):
    """ Removes the stderr StreamHandler from root logger (if there). """
    if logger is None:
        logger = logging.root

    for h in list(logger.handlers):
        if _is_stderr_handler(h):
            logger.removeHandler(h)


def _is_stderr_handler(handler):
    return isinstance(handler, logging.StreamHandler) and handler.stream == sys.stderr


def enable_file(filename, logger=None, file_handler=None, rotate=False, **kwargs):
    """
    Adds a FileHandler to root logger, to enable logging to ``filename``.
    If rotate=True, will create a daily-rotating file handler (filename should contain '*',
    which is replaced with the date).
    """
    if file_handler is None:
        if rotate:
            file_handler = DailyRotatingFileHandler(filename, **kwargs)
        else:
            file_handler = FileHandler(filename, **kwargs)
    return _add_logging_handler(file_handler, logger=logger)


def _add_logging_handler(handler, logger=None):
    if logger is None:
        logger = logging.root
    if handler.formatter is None:
        handler.setFormatter(formatter)
    logger.addHandler(handler)


################################################################################
