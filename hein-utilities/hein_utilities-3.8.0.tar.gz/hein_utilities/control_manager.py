"""
Contextual action managers
"""
import re
import logging
from typing import Callable, Pattern

# regex patterns
start_pattern = re.compile('start', re.IGNORECASE)
pause_pattern = re.compile('pause|suspend', re.IGNORECASE)
stop_pattern = re.compile('stop|halt|quit', re.IGNORECASE)
resume_pattern = re.compile('resume', re.IGNORECASE)
status_pattern = re.compile('status', re.IGNORECASE)

# logger
logger = logging.getLogger(__name__)


def do_nothing(*args, **kwargs):
    """function that does nothing"""
    logger.debug('doing nothing')
    pass


def return_empty(*args, **kwargs):
    """function that returns an empty string"""
    return ''


class ControlManager:
    # catch patterns
    start_pattern: Pattern = start_pattern
    pause_pattern: Pattern = pause_pattern
    stop_pattern: Pattern = stop_pattern
    resume_pattern: Pattern = resume_pattern
    status_pattern: Pattern = status_pattern

    def __init__(self,
                 start_action: Callable = do_nothing,
                 stop_action: Callable = do_nothing,
                 resume_action: Callable = do_nothing,
                 pause_action: Callable = do_nothing,
                 status_query: Callable = return_empty,
                 ):
        """
        A control manager for executing steps contextually. Context actions can be assigned as properties of the manager
        so that they can be executed by the appropriate trigger.

        :param start_action: callable action to execute on a start trigger
        :param stop_action: callable action to execute on a stop trigger
        :param resume_action: callable action to execute on a resume trigger
        :param pause_action: callable action to execute on a pause trigger
        :param status_query: callable which returns a string representing the status of the thing being controlled
        """
        self._start_action = do_nothing
        self._pause_action = do_nothing
        self._resume_action = do_nothing
        self._stop_action = do_nothing
        self._status_query = return_empty
        self.start_action = start_action
        self.stop_action = stop_action
        self.resume_action = resume_action
        self.pause_action = pause_action
        self.status_query = status_query

    def __str__(self):
        return f'{self.__class__.__name__}'

    @property
    def start_action(self) -> Callable:
        """the callable which is executed on start catches"""
        return self._start_action

    @start_action.setter
    def start_action(self, value: Callable):
        if callable(value) is False:
            raise TypeError(f'{value} is not callable')
        self._start_action = value

    @start_action.deleter
    def start_action(self):
        self._start_action = do_nothing

    @property
    def pause_action(self) -> Callable:
        """the callable which is executed on pause catches"""
        return self._pause_action

    @pause_action.setter
    def pause_action(self, value: Callable):
        if callable(value) is False:
            raise TypeError(f'{value} is not callable')
        self._pause_action = value

    @pause_action.deleter
    def pause_action(self):
        self._pause_action = do_nothing

    @property
    def resume_action(self) -> Callable:
        """the callable which is executed on resume catches"""
        return self._resume_action

    @resume_action.setter
    def resume_action(self, value: Callable):
        if callable(value) is False:
            raise TypeError(f'{value} is not callable')
        self._resume_action = value

    @resume_action.deleter
    def resume_action(self):
        self._resume_action = do_nothing

    @property
    def stop_action(self) -> Callable:
        """the callable which is executed on stop catches"""
        return self._stop_action

    @stop_action.setter
    def stop_action(self, value: Callable):
        if callable(value) is False:
            raise TypeError(f'{value} is not callable')
        self._stop_action = value

    @stop_action.deleter
    def stop_action(self):
        self._stop_action = do_nothing

    @property
    def status_query(self) -> Callable:
        """the callable which is used to retrieve a status string"""
        return self._status_query

    @status_query.setter
    def status_query(self, value: Callable):
        if callable(value) is False:
            raise TypeError(f'{value} is not callable')
        self._status_query = value

    @status_query.deleter
    def status_query(self):
        self._status_query = return_empty
