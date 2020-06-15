"""Copy-paste/identical to the mixins module from the north_utils package version 0.0.13"""

import logging
from threading import Thread
from typing import Optional

logger = logging.getLogger(__name__)


class Loggable:
    def __init__(self, logger: logging.Logger=logger, name: Optional[str]=None, log_init: bool=True):
        self.logger = logger.getChild(self.__class__.__name__) if name is None else name
        if log_init:
            self.logger.debug('__init__')


class RunnableError(Exception):
    pass


class Runnable(Loggable):
    def __init__(self, logger: logging.Logger=logger, thread_timeout: int=1) -> None:
        Loggable.__init__(self, logger=logger)

        self.thread = Thread(target=self.run, daemon=True)
        self.thread_timeout = thread_timeout
        self.running = False

    def run(self) -> None:
        pass

    def start(self) -> None:
        self.logger.debug('start')

        if self.thread.is_alive():
            raise RunnableError(f'Runnable "{self.__class__.__name__}" already running')

        self.running = True
        self.thread.start()

    def stop(self) -> None:
        self.logger.debug('stop')

        if self.running:
            self.running = False
            self.thread.join(self.thread_timeout)
            self.thread = Thread(target=self.run, daemon=True)
