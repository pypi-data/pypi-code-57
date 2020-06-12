import time
import maya
import datetime
import humanize
import uuid

from pprint import pprint
from typing import Dict, Any
from addict import Dict as ADict

from jamboree import Jamboree
from loguru import logger
from see137.common import AddictComponent, AddictWithManagerComponent
from see137.search.backtesting import BacktestManager



class LoadBacktestComponent(AddictWithManagerComponent):
    """Load Backtest 

        Load the configuration information for a given backtest.
    """
    def __init__(self):
        super().__init__()
        self.name = "Load Backtest"
        # Backtest configuration dict. Can be saved into the database immediately.
        
        self.required_items = {
            "backtest": str
        }



    def process(self, item:ADict):
        """Given an id inside of the item dictionary `backtest`, get information using that id

        Arguments:
            item {ADict} -- Addict modified dictionary. Save's according to backtest data.

        Returns:
            ADict -- Modified dictionary with action and percentage inside of it
        """
        return item


    def step(self, item:ADict, **settings):
        return super().step(item, **settings)

if __name__ == "__main__":
    response = None
    # for _ in range(100):
    sample_backtest_dict = ADict(backtest=uuid.uuid4().hex)

    load_backtest = LoadBacktestComponent()
    load_backtest.processor = Jamboree()
    response = load_backtest.step(sample_backtest_dict)
    
    
    
    pprint(response)
    
