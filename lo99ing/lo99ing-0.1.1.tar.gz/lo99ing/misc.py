"""
Misc functions used in this package.
"""

import logging
from pathlib import Path


################################################################################
# thread safety

logging_lock = logging._lock


################################################################################
# string formatting

def truncate(x, maxlen=1000):
    """
    >>> truncate('1234567890', 8)
    '1234 ...'
    >>> truncate('1234567890', 10)
    '1234567890'
    """
    if len(x) > maxlen:
        suffix = ' ...'
        return '%s%s' % (x[:maxlen - len(suffix)], suffix)
    else:
        return x


def join_lines(s):
    """ replaces newlines with spaces. """
    return ' '.join(line.strip() for line in s.splitlines())


def oneline(s, **kwargs):
    s = str(s)
    return join_lines(truncate(s, **kwargs))


################################################################################
# exception related

def get_exception_kwargs(e):
    """ Extracts extra info (attributes) from an exception object. """
    kwargs = {}
    for attr, value in vars(e).items():
        if not attr.startswith('_') and attr not in ('args', 'message'):
            kwargs[attr] = value
    return kwargs


def format_exception(e):
    """ Returns a string which includes both exception-type and its str() """
    try:
        exception_str = str(e)
    except Exception:
        try:
            exception_str = repr(e)
        except Exception:
            exception_str = '(error formatting exception)'
    return '%s - %s' % (e.__class__.__name__, exception_str)


################################################################################
# module related

def is_installed_module(module_filename):
    """
    Checks if a module is "installed" (e.g. using pip), as opposed to a "local" module, belonging
    to user's env (e.g. local development tree).
    """
    return any(
        p.name in ['site-packages', 'dist-packages']
        for p in Path(module_filename).parents
    )


################################################################################
