"""
Definition of lo99ing's custom logger class.
"""

import sys
import inspect
import logging
import lo99ing

from .level import set_log_level_override
from .misc import oneline, get_exception_kwargs, format_exception, is_installed_module


################################################################################

class Lo99er(logging.Logger):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_default_level()

    ################################################################################
    # Logger overrides

    def _log(self, level, msg, args, exc_info=None, extra=None):

        # automatically format exceptions properly (if passed directly as arguments):
        args = tuple([
            format_exception(a) if isinstance(a, Exception) else a
            for a in args
        ])

        # call super:
        super()._log(level, msg, args, exc_info=exc_info, extra=extra)

    def exception(self, msg, *args, exc_info=None, **kwargs):

        # get exc_info and exc_obj:
        exc_obj = None
        if exc_info is not None:
            if isinstance(exc_info, BaseException):
                exc_obj = exc_info
            elif isinstance(exc_info, tuple):
                exc_obj = exc_info[1]
        if exc_obj is None:
            exc_info = sys.exc_info()
            exc_obj = exc_info[1]

        # call super:
        super().exception(msg, *args, exc_info=exc_info, **kwargs)

        # add exception attributes:
        exc_kwargs = get_exception_kwargs(exc_obj)
        for attr, v in exc_kwargs.items():
            self.error('\t%s.%s = %s' % (exc_obj.__class__.__name__, attr, oneline(v)))

    def getChild(self, suffix):
        from lo99ing import get_logger

        if self.root is not self:
            suffix = '.'.join((self.name, suffix))
        return get_logger(suffix)  # using get_logger() instead of self.manager.getLogger()

    ################################################################################
    # log level

    def _set_default_level(self):
        """
        Sets log-level of self to WARNING if logger is created from an "installed" ("3rd party")
        module (as opposed to a "local" module in user's development tree), and to INFO otherwise.
        """
        logging_packages = [logging.__package__, lo99ing.__package__]
        try:
            # find caller frame, i.e. deepest frame which is not in logging/lo99ing
            frame = None
            for f in inspect.stack():
                if f.frame.f_globals.get('__package__') not in logging_packages:
                    frame = f
                    break
            if is_installed_module(frame.filename):
                # module belonging an installed package. default is warning
                level = logging.WARNING
            else:
                # presumably a "local" script/module, belonging to the user running this.
                # default is info
                level = logging.INFO
        except Exception:
            level = logging.INFO
        self.setLevel(level)

    def set_log_level_override(self, level):
        """
        Override this logger's log-level.
        Call with level=None to reset the override.
        """
        return set_log_level_override(self.name, level)

    ################################################################################
    # utilities

    def prefixed(self, prefix):
        """ Returns a new adaptor (logger-like) object, which adds `prefix` to logged messages. """
        return prefixed(self, prefix)

    def TRACE(self, *args, **kwargs):
        """
        A convenience method for logging current filename and line num (and optional extra info).
        Useful for "printf-debugging" (aka "trace-debugging").
        """
        try:
            fn, lno, _, _ = self._findCaller()
        except ValueError:
            fn, lno = "(unknown file)", 0

        args_str = ''
        if args:
            args_str = '  '.join(repr(a) for a in args)
        kwargs_str = ''
        if kwargs:
            kwargs_str = '  '.join('%s=%r' % item for item in kwargs.items())
        self.critical('TRACE %s:%s   %s   %s', fn, lno, args_str, kwargs_str)

    ################################################################################
    # other

    def __repr__(self):
        return '<%s %r [%s]>' % (
            type(self).__name__, self.name, logging.getLevelName(self.level))

    def _findCaller(self, *args, **kwargs):
        # NOTE: we don't call self.findCaller() directly from TRACE, because it only
        # works if called from the "correct" relative depth from user's call.
        return self.findCaller(*args, **kwargs)


################################################################################
# prefixed

class _PrefixedAdapter(logging.LoggerAdapter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            initial_prefix = self.logger.extra['prefix']
        except (AttributeError, KeyError):
            initial_prefix = ''
        self.extra['prefix'] = '%s%s ' % (initial_prefix, self.prefix)

    @property
    def prefix(self):
        return self.extra['prefix']

    def process(self, msg, kwargs):
        return (self.prefix + msg), kwargs

    def __repr__(self):
        return '<%s %r %s>' % (type(self).__name__, self.logger, self.prefix)

    # make this more logger-like, for prefix chaining to work:

    def prefixed(self, prefix):
        return prefixed(self, prefix)

    @property
    def manager(self):
        return self.logger.manager

    @property
    def _log(self):
        return self.logger._log

    def getChild(self, *args, **kwargs):
        child_logger = self.logger.getChild(*args, **kwargs)
        return type(self)(child_logger, {'prefix': self.prefix})

    def set_log_level_override(self, *args, **kwargs):
        return self.logger.set_log_level_override(*args, **kwargs)

    def TRACE(self, *args, **kwargs):
        return self.logger.TRACE(*args, **kwargs)


def prefixed(logger, prefix):
    """ Returns a new adaptor (logger-like) object, which adds `prefix` to messages it logs. """
    return _PrefixedAdapter(logger, {'prefix': prefix})


################################################################################
