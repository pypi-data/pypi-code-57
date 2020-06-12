import uuid
import maya

from typing import Optional
from jamboree import Jamboree
from jamboree.base.processors.abstracts import Processor
from jamboree.handlers.abstracted.search import ParameterizedSearch


from see137.search.backtesting import CreateAccessor, InfoAccessor, UpdateAccessor, RemoveAccessor
from see137.common.injectable import InjectableObject
from loguru import logger


class BacktestManager(InjectableObject):
    """ 
        # Backtest Search


    """
    def __init__(self):
        self._processor: Optional[Processor] = None
        self._create = CreateAccessor()
        self._update = UpdateAccessor()
        self._remove = RemoveAccessor()
        self._info = InfoAccessor()

    
    # @property
    # def processor(self):
    #     if self._processor is None:
    #         raise AttributeError("Injected processor hasn't been set. ")
    #     return self._processor

    # @processor.setter
    # def processor(self, _processor):
    #     self._processor = _processor

    @property
    def create(self):
        self._create.processor = self.processor
        return self._create
    
    @property
    def update(self):
        self._update.processor = self.processor
        return self._update
    
    @property
    def remove(self):
        self._remove.processor = self.processor
        return self._remove

    @property
    def info(self):
        self._info.processor = self.processor
        return self._info


def main_testing():
    pass

if __name__ == "__main__":
    main_testing()