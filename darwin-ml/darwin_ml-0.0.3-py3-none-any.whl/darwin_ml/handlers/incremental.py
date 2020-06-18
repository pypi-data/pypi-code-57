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
from jamboree.utils.support.search import querying
from loguru import logger

from darwin_ml.models import OnlineModels, StateSpaceModel

# logger.disable(__name__)


class IncrementalEngine(FileEngine):
    """ 
        Save and load incremental learning models dynamically by metadata and ID.

        Use to get rolling statistics for the 

        Uses context to make decisions and provide some clean up during the process :
        ```
            with strategy as strat:
                strat.step(dataframe)
        ```
    """
    def __init__(self, processor=None, **kwargs):
        super().__init__(processor=processor, **kwargs)
        self.entity = "incremental_models"
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
        return self.models

    def custom_post_load(self, item):
        self.current_strategy = item

    @property
    def models(self):
        if self.current_strategy is not None:
            return self.current_strategy
        raise AttributeError("No model set and found")

    def file_from_dict(self, item: Dict):
        reloaded = IncrementalEngine(processor=self.processor,
                                     name=item.name,
                                     category=item.category,
                                     subcategories=item.subcategories,
                                     submetatype=item.submetatype,
                                     abbreviation=item.abbreviation)
        return reloaded

    def reset(self):
        super().reset()
        logger.warning(self.metaid)
        if self.file_reset == True and self.current_strategy is None:
            if self.blobfile is not None:
                self.current_strategy = self.blobfile


class SampleStrategy(object):
    def step(self, df: pd.DataFrame):
        """ Preprocess the dataframe and make decisions using the step function. """
        return random.choice([0, 1, 2])


# @logger.catch
def main_strategy():
    jam_processor = Jamboree()
    strat = StateSpaceModel()
    incremental_engine = IncrementalEngine(processor=jam_processor,
                                           name="SAMPLE_NAMES",
                                           category="SAMCATSASSSS",
                                           subcategories={"sam": "ple"},
                                           submetatype="OTHER_SMAPLE__",
                                           abbreviation="SAP",
                                           blobfile=strat)
    incremental_engine.reset()
    while True:
        # We'd `pick` a strategy by `episode`. We'd first get an episode, get the strategy, then get the strategy, then pass in the data
        first_model = incremental_engine.first(name="SAMPLE_NAMES",
                                               category="SAMCATSASSSS",
                                               submetatype="OTHER_SMAPLE__")
        with first_model as model:
            logger.warning(model)


if __name__ == "__main__":
    main_strategy()
