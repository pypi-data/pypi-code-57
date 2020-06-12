import random
import time
import uuid
from pprint import pprint
from typing import Any, List, Optional

import maya
import pandas as pd
from addict import Dict
from jamboree import Jamboree
from jamboree.handlers.complex.engines import FileEngine
# from jamboree.middleware.procedures import (ModelProcedureAbstract,
#                                             ModelProcedureManagement,
#                                             ProcedureAbstract,
#                                             ProcedureManagement)
from jamboree.utils.support.search import querying
from loguru import logger

# logger.disable(__name__)

class StrategyEngine(FileEngine):
    """ 
        Save and load strategies dynamically by metadata and ID.

        Use to make decisions on multiple assets. 

        Uses context to make decisions and provide some clean up during the process :
        ```
            with strategy as strat:
                strat.step(dataframe)
        ```
    """

    def __init__(self, processor=None, **kwargs):
        super().__init__(processor=processor, **kwargs)
        self.entity = "deployed_strategies"
        self.current_strategy = None
        

    def init_specialized(self, **kwargs):
        super().init_specialized(**kwargs)

    def verify(self):
        """ Disabling verify. """
        pass

    def open_context(self):
        if not self.file_reset:
            self.reset()
        

    def close_context(self):
        pass


    def enterable(self):
        """ Return the object we want to enter into """
        return self.strategy

    def custom_post_load(self, item):
        self.current_strategy = item

    @property
    def strategy(self):
        if self.current_strategy is not None:
            return self.current_strategy
        raise AttributeError("No strategy set and found")
    
    def file_from_dict(self, item:Dict):
        # print(item)
        reloaded = StrategyEngine(
            processor=self.processor,
            name=item.name,
            category=item.category,
            subcategories=item.subcategories,
            submetatype=item.submetatype,
            abbreviation=item.abbreviation
        )
        return reloaded

    def reset(self):
        super().reset()
        if self.file_reset == True and self.current_strategy is None:
            if self.blobfile is not None:
                self.current_strategy = self.blobfile

class SampleStrategy(object):
    def step(self, df:pd.DataFrame):
        """ Preprocess the dataframe and make decisions using the step function. """
        return random.choice([0, 1, 2])

@logger.catch
def main_strategy():
    jam_processor = Jamboree()
    strat = SampleStrategy()
    strat_engine = StrategyEngine(
        processor=jam_processor,
        name="SAMPLE_NAME",
        category="SAMCATSASS",
        subcategories={"sam": "ple"},
        submetatype="OTHER SMAPLE",
        abbreviation="SAP",
        blobfile=strat
    )
    strat_engine.reset()
    while True:
        # We'd `pick` a strategy by `episode`. We'd first get an episode, get the strategy, then get the strategy, then pass in the data 
        strategy = strat_engine.first(
            name="SAMPLE_NAME",
            category="SAMCATSASS",
            submetatype="OTHER SMAPLE"
        )
        logger.success(strategy.metaid)
        with strategy as stray:
            logger.warning(stray.step(1223))

if __name__ == "__main__":
    main_strategy()
