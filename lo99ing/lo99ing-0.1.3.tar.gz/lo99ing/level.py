"""
Tools for working with log levels (and overrides).
"""

import logging
from .misc import logging_lock


################################################################################
# basic log-level actions

def get_log_level(name):
    return logging.getLogger(name).level


def set_log_level(name, level):
    level = to_level(level)
    logging.getLogger(name).setLevel(level)


def is_enabled(logger, level):
    logging_level = to_level(level)
    return logger.isEnabledFor(logging_level)


def to_level(level):
    if isinstance(level, int):
        logging_level = level
    elif isinstance(level, str):
        try:
            logging_level = getattr(logging, level.upper())
        except KeyError:
            raise ValueError('invalid level', level) from None
    else:
        raise TypeError('invalid level', level)
    return logging_level


################################################################################
# log level overrides

class LogLevelManager:
    """
    Keeps track of log level: for each logger, it stores initial and override levels.
    """

    def __init__(self):
        self.initials = {}
        self.overrides = {}

    def set_initial(self, name, level):
        assert level is not None, (name, level)
        self.initials.setdefault(name, level)

    def get_initial(self, name):
        return self.initials.get(name)

    def has_initial(self, name):
        return name in self.initials

    def set_override(self, name, level):
        assert level is not None, (name, level)
        self.overrides[name] = level

    def get_override(self, name):
        return self.overrides.get(name)

    def clear_override(self, name):
        self.overrides.pop(name, None)

    def get_effective(self, name):
        try:
            return self.overrides[name]
        except KeyError:
            return self.initials.get(name, None)

    def get_all_overrides(self):
        return dict(self.overrides)

    def restore_overrides(self, overrides):
        for name, level in overrides.items():
            self.set_override(name, level)


log_level_manager = LogLevelManager()


def get_log_level_override(name):
    """ Returns the current override for given logger, or None. """
    with logging_lock:
        return log_level_manager.get_override(name)


def set_log_level_override(name, level):
    """
    Override log level of given logger.
    If ``level is None``, will reset, i.e. clear existing override.
    """
    with logging_lock:
        if level is None:
            log_level_manager.clear_override(name)
        else:
            level = to_level(level)
            log_level_manager.set_override(name, level)

        is_initialized = log_level_manager.has_initial(name)
        if is_initialized:
            eff_level = log_level_manager.get_effective(name)
            set_log_level(name, eff_level)


def get_log_level_overrides():
    """ Return all current log-level overrides, as a name->level dict. """
    with logging_lock:
        return log_level_manager.get_all_overrides()


def restore_log_level_overrides(overrides):
    """
    Set multiple log-level overrides.
    :param overrides: the value returned by ``get_all_overrides``.
    """
    with logging_lock:
        return log_level_manager.restore_overrides(overrides)


################################################################################
