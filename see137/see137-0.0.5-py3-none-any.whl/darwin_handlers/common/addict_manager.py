import uuid
from loguru import logger
from typing import List, Dict, Tuple, Any
from addict import Dict as ADict
from see137.common import ComponentAbstract, AddictComponent
from see137.search.backtesting import BacktestManager


class AddictWithManagerComponent(AddictComponent):
    """
        A component that centers around using dictionaries and addict.
    """
    def __init__(self):
        super().__init__()
        self.__manager = BacktestManager()
    
    @property
    def manager(self):
        self.__manager.processor = self.processor
        return self.__manager

if __name__ == "__main__":
    comp = AddictWithManagerComponent()
    sample_param = ADict(episode=uuid.uuid4().hex)
    print(comp.step(sample_param, asset=uuid.uuid4().hex))