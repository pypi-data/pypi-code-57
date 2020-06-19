#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Copyright (C) 2019, 2020 Brandon M. Pace
#
# This file is part of logcontrol
#
# logcontrol is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# logcontrol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with logcontrol.
# If not, see <https://www.gnu.org/licenses/>.

"""module for creating and storing loggers"""


import logging
import threading

from logging.handlers import RotatingFileHandler
from typing import Dict, List, Optional, Set, Union
from .constants import CONSOLE_HANDLER_NAME, DEFAULT_CONSOLE_LOG_FORMAT, DEFAULT_LOG_FORMAT, ROOT, ROOT_LOGGER
from .validation import validate_file_path, validate_group_name, validate_handler_object, validate_logger_object


class LoggerGroup:
    def __init__(self, name: str):
        validate_group_name(name)
        self._name = name
        self._lock = threading.RLock()
        if name == ROOT:
            self._loggers: Set[logging.Logger] = {ROOT_LOGGER}
            self._is_root = True
            self._level = ROOT_LOGGER.getEffectiveLevel()
            ROOT_LOGGER.setLevel(self._level)
        else:
            self._loggers: Set[logging.Logger] = set()
            self._is_root = False
            self._level: int = logging.WARNING

        self._console_handler: Optional[logging.StreamHandler] = None
        self._file_handlers: Dict[str, logging.FileHandler] = {}
        self._handlers: Set[logging.Handler] = set()
        self._propagate = True  # updated when first logger is added. Not relevant for root logger.

    def __contains__(self, item: Union[logging.Handler, logging.Logger]) -> bool:
        with self._lock:
            if isinstance(item, logging.Logger):
                return item in self._loggers
            elif isinstance(item, logging.Handler):
                return item in self._handlers
            else:
                raise TypeError(
                    f"'in <{type(self).__class__.__name__}>' requires logging.Logger or logging.Handler for left operand, not {type(item)}"
                )

    def __iter__(self):
        return self._loggers.__iter__()

    def __len__(self) -> int:
        return len(self._loggers)

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.name)

    def add_handler(self, handler: logging.Handler):
        with self._lock:
            validate_handler_object(handler)
            for logger in self:
                logger.addHandler(handler)

            self._handlers.add(handler)

            if self._is_root:
                _logger.debug(f"handler '{handler}' added to root logger")
            else:
                _logger.debug(f"handler '{handler}' added to logger group {self._name}")

    def add_log_file(self, file_path: str, fmt: str = None, datefmt: str = None, max_size: int = 5242880, roll_count: int = 9):
        with self._lock:
            validate_file_path(file_path)
            if file_path in self._file_handlers:
                if self._is_root:
                    raise ValueError(f"root logger is already logging to path '{file_path}'")
                else:
                    raise ValueError(f"group {self._name} already logging to path '{file_path}'")
            format_string = (fmt if fmt else DEFAULT_LOG_FORMAT)
            formatter = logging.Formatter(fmt=format_string, datefmt=datefmt)
            rotation_handler = RotatingFileHandler(file_path, maxBytes=max_size, backupCount=roll_count)
            rotation_handler.setFormatter(formatter)
            self._file_handlers[file_path] = rotation_handler
            self.add_handler(rotation_handler)

    def add_logger(self, logger: logging.Logger):
        if self._is_root:
            raise RuntimeError(f"Adding loggers to the root group is not allowed")

        validate_logger_object(logger)

        with self._lock:
            if logger in self:
                raise ValueError(f"Logger '{logger}' already added to this group")

            if self._loggers:
                logger.setLevel(self._level)
                logger.propagate = self._propagate
                for handler in self._handlers:
                    logger.addHandler(handler)
            else:
                # This is the first logger in the group, will update initial group configuration
                self._level = logger.getEffectiveLevel()
                logger.setLevel(self._level)
                self._propagate = bool(logger.propagate)

            self._loggers.add(logger)

    def disable_propagation(self):
        if self._is_root:
            raise RuntimeError(f"irrelevant modification to root logger")
        with self._lock:
            if self._propagate:
                for logger in self:
                    logger.propagate = False
                _logger.debug(f"propagation disabled for logger group '{self._name}'")
                self._propagate = False
            else:
                _logger.warning(f"propagation already disabled for group '{self._name}'")

    def enable_propagation(self):
        if self._is_root:
            raise RuntimeError(f"irrelevant modification to root logger")
        with self._lock:
            if self._propagate:
                _logger.warning(f"propagation already enabled for group '{self._name}'")
            else:
                for logger in self:
                    logger.propagate = True
                _logger.debug(f"propagation enabled for logger group '{self._name}'")

    @property
    def level(self):
        return self._level

    @property
    def log_files(self) -> List[str]:
        return list(self._file_handlers)

    def log_to_console(self, fmt: str = None, datefmt: str = None, level: int = None):
        with self._lock:
            if self._console_handler:
                self.remove_handler(self._console_handler)
                self._console_handler = None
            log_format = (DEFAULT_CONSOLE_LOG_FORMAT if fmt is None else fmt)
            formatter = logging.Formatter(fmt=log_format, datefmt=datefmt)
            console_handler = logging.StreamHandler()
            console_handler.name = CONSOLE_HANDLER_NAME
            console_handler.setFormatter(formatter)
            if isinstance(level, int):
                console_handler.level = level
            elif level is not None:
                raise TypeError(f"Expected int level, got type: '{type(level)}'")
            self._console_handler = console_handler
            self.add_handler(console_handler)

    @property
    def logging_to_console(self) -> bool:
        return self._console_handler is not None

    @property
    def name(self) -> str:
        return self._name

    @property
    def propagate(self) -> bool:
        return self._propagate

    def remove_handler(self, handler: logging.Handler):
        validate_handler_object(handler)
        with self._lock:
            if handler not in self:
                _logger.warning(f"handler '{handler}' not found")
                return

            for logger in self:
                logger.removeHandler(handler)

            self._handlers.discard(handler)

            if self._is_root:
                _logger.debug(f"handler '{handler}' removed from root logger")
            else:
                _logger.debug(f"handler '{handler}' removed from logger group {self._name}")

    def remove_log_file(self, file_path: str):
        with self._lock:
            if file_path in self._file_handlers:
                self.remove_handler(self._file_handlers[file_path])
                del self._file_handlers[file_path]
            else:
                if self._is_root:
                    raise ValueError(f"root logger has no handler for file '{file_path}'")
                else:
                    raise ValueError(f"group {self._name} has no handler for file '{file_path}'")

    def set_level(self, level: Union[int, str]):
        if isinstance(level, int):
            level_name = logging.getLevelName(level)
        elif isinstance(level, str):
            level_name = level
            level = logging.getLevelName(level_name)
            if isinstance(level, str):
                raise ValueError(f"Log level '{level_name}' does not match any logging module built-in level")
        else:
            raise TypeError(f"Expected int or str, got type '{type(level)}' with value '{level}'")

        with self._lock:
            for logger in self:
                logger.setLevel(level)
            self._level = level
            if self._is_root:
                _logger.debug(f"log level set to '{level_name}'")
            else:
                _logger.debug(f"log level set to '{level_name}' for logger group '{self._name}'")

    def stop_logging_to_console(self):
        with self._lock:
            if self._console_handler:
                self.remove_handler(self._console_handler)
                self._console_handler = None
            else:
                if self._is_root:
                    _logger.warning("root logger was not logging to console, pointless call")
                else:
                    _logger.warning(f"group '{self._name}' was not logging to console, pointless call")


_logger = logging.getLogger(__name__)
logger_groups: Dict[str, LoggerGroup] = {}
logger_lock = threading.RLock()
loggers: Set[logging.Logger] = set()
root_logger_group = LoggerGroup(ROOT)


def add_handler(handler: logging.Handler, group: str = None):
    """Add a log handler to a group of loggers (or the root logger if no group provided)"""
    if group is None:
        root_logger_group.add_handler(handler)
    else:
        with logger_lock:
            validate_group_exists(group)
            logger_groups[group].add_handler(handler)


def current_level(group: str = None) -> int:
    """
    Get current integer log level for root logger or a specific group of loggers.
    If no group is passed, the level for the root logger is returned.
    """
    if group is None:
        return root_logger_group.level
    else:
        with logger_lock:
            validate_group_exists(group)
            return logger_groups[group].level


def current_level_name(group: str = None) -> str:
    """
    Get current string log level name for root logger or a specific group of loggers.
    If no group is passed, the level for the root logger is returned.
    """
    level = current_level(group)
    return logging.getLevelName(level)


def disable_propagation(group: str):
    """
    Disable propagation for a specific group of loggers.
    This means no logger lower in the hierarchy will process messages from it and its children.
    """
    with logger_lock:
        validate_group_exists(group)
        logger_groups[group].disable_propagation()


def enable_propagation(group: str):
    """
    Enable propagation for a specific group of loggers.
    This means any logger lower in the hierarchy will process messages from it and its children.
    """
    with logger_lock:
        validate_group_exists(group)
        logger_groups[group].enable_propagation()


def group_levels() -> Dict[str, int]:
    """
    Get a dictionary with group names as keys and the integer levels as values
    """
    with logger_lock:
        return {group: group_object.level for group, group_object in logger_groups.items()}


def group_level_names() -> Dict[str, str]:
    """
    Get a dictionary with group names as keys and string level name as values
    This can be useful for populating a debug options window that allows configuring the different groups.
    """
    with logger_lock:
        return {group: logging.getLevelName(level) for group, level in group_levels().items()}


def group_names() -> List[str]:
    """
    Get a sorted list of group names that have been added
    """
    with logger_lock:
        return sorted([group for group in logger_groups])


def has_handler(handler: logging.Handler, group: str = None) -> bool:
    """Check if a log handler is assigned to a group of loggers (or the root logger if no group provided)"""
    validate_handler_object(handler)
    if group is None:
        return handler in root_logger_group
    else:
        with logger_lock:
            validate_group_exists(group)
            return handler in logger_groups[group]


def log_files(group: str = None) -> List[str]:
    """
    Get any set log files for the root logger (or group, if given)
    """
    with logger_lock:
        if group is None:
            group_object = root_logger_group
        else:
            validate_group_exists(group)
            group_object = logger_groups[group]
        return group_object.log_files


def log_to_console(group: str = None, fmt: str = None, datefmt: str = None, level: int = None):
    """
    Enable printing log items to the console
    If a group name is passed, then loggers in that group will log to console.
    If a group name is not passed, the root logger will log to console.
    If a format string is passed to via fmt or datefmt, it will be used.
    If a format is not passed, a default is used.
    (see logging.Formatter and LogRecord attributes documentation for more information about format strings)
    NOTE: If you do not have a handler for the root logger, you may see all loggers output on the console.
    """
    if group is None:
        root_logger_group.log_to_console(fmt=fmt, datefmt=datefmt, level=level)
    else:
        with logger_lock:
            validate_group_exists(group)
            logger_groups[group].log_to_console(fmt=fmt, datefmt=datefmt, level=level)


def logging_to_console(group: str = None) -> bool:
    """
    Check if a group or root logger is printing log items to the console
    If a group name is passed, then that group's value is returned.
    If a group name is not passed, the root logger's value is returned.
    """
    if group is None:
        return root_logger_group.logging_to_console
    else:
        with logger_lock:
            validate_group_exists(group)
            return logger_groups[group].logging_to_console


def propagation_enabled(group: str) -> bool:
    """
    Check if a group is propagating to lower loggers
    """
    with logger_lock:
        validate_group_exists(group)
        return logger_groups[group].logging_to_console


def register_logger(logger: logging.Logger, group: str):
    """
    Add a logger to be controlled. The group name can be a user-friendly one if you wish.
    """
    validate_logger_object(logger)
    if logger is ROOT_LOGGER:
        raise RuntimeError(f"The root logger is not allowed to be assigned to a group")
    elif group == ROOT:
        raise RuntimeError(f"The root group name is reserved and must not be used")
    with logger_lock:
        if logger in loggers:
            raise ValueError(f"logger already registered: {logger}")

        if group in logger_groups:
            logger_groups[group].add_logger(logger)
        else:
            logger_groups[group] = LoggerGroup(group)
            logger_groups[group].add_logger(logger)

        loggers.add(logger)


def remove_handler(handler: logging.Handler, group: str = None):
    """Remove a log handler from a group of loggers (or the root logger if no group provided)"""
    if group is None:
        root_logger_group.remove_handler(handler)
    else:
        with logger_lock:
            validate_group_exists(group)
            logger_groups[group].remove_handler(handler)


def remove_log_file(file_path: str, group: str = None):
    """
    Remove a previously set log file for the root logger (or group, if given)
    """
    with logger_lock:
        if group is None:
            group_object = root_logger_group
        else:
            validate_group_exists(group)
            group_object = logger_groups[group]
        group_object.remove_log_file(file_path)


def set_level(level: Union[int, str], group: str = None):
    """
    Set log level for root logger or a specific group of loggers.
    level is as seen in Python's logging module documentation (e.g. logging.DEBUG, logging.WARNING, logging.INFO)
    The string names of built-in log levels are also accepted, but using the integer constants is recommended.
    If no group is passed, the level is configured for the root logger.
    """
    if group is None:
        root_logger_group.set_level(level)
    else:
        with logger_lock:
            validate_group_exists(group)
            logger_groups[group].set_level(level)


def set_log_file(file_path: str, group: str = None, fmt: str = None, datefmt: str = None, max_size: int = 5242880, roll_count: int = 9):
    """
    Set the log file for the root logger (or group, if given)

    The file path is the destination log file
    If a group name is provided, it will only apply to the specific group.
    If a format string is passed to via fmt or datefmt, it will be used.
    If a format is not passed, a default is used.
    (see logging.Formatter and LogRecord attributes documentation for more information about format strings)
    The max size is in bytes
    The roll count determines how many files beyond the current log are kept (e.g. log_file.1, log_file.2, etc.)
    """
    with logger_lock:
        if group is None:
            group_object = root_logger_group
        else:
            validate_group_exists(group)
            group_object = logger_groups[group]
        group_object.add_log_file(
            file_path=file_path, fmt=fmt, datefmt=datefmt, max_size=max_size, roll_count=roll_count
        )


def stop_logging_to_console(group: str = None):
    """
    Disable printing log items to the console
    If a group name is passed, then loggers in that group will stop logging to console.
    If a group name is not passed, the root logger will stop logging to console.
    NOTE: If you do not have a handler for the root logger, you may see all loggers output on the console.
    """
    if group is None:
        root_logger_group.stop_logging_to_console()
    else:
        with logger_lock:
            validate_group_exists(group)
            logger_groups[group].stop_logging_to_console()


def validate_group_exists(group: str):
    """Internal function to validate that a group has been added"""
    if group not in logger_groups:
        raise ValueError(f"no logger group with name: '{group}'")
