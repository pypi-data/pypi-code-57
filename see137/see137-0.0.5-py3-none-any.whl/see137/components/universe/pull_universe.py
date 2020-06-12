# As a user, I'd like to pull the attached process strategy, pull the data, process the data, get a decision from that data
from addict import Dict as ADict
from typing import List
from jamboree.handlers.default.multi import MultiDataManagement
from see137.handlers.strategy.core import StrategyEngine
from see137.common import Pipeline, ComponentAbstract, AddictWithManagerComponent
from loguru import logger

class PullUniverse(AddictWithManagerComponent):
    """
        Pulls all of the universe asset_ids
    """
    def __init__(self):
        super(PullUniverse, self).__init__()
        self.required_settings = {}

        # Backtest configuration dict. Can be saved into the database immediately.
        
        self.required_items = {
            "config": dict
        }

        self.__private_multi = MultiDataManagement()
        self.mult_handler = None
    
    def check_prev(self, item):
        return super().check_prev(item)

    def check_all(self, item):
        return super().check_all(item)
    
    def check_item(self, item):
        return super().check_item(item)
    
    @property
    def multi(self):
        self.__private_multi.processor = self.processor
        return self.__private_multi

    def check_multi(self, universe:str):
        """Check the if the multi-data handler exists. Should return none if not.  

        Arguments:
            universe {str} -- [description]

        Returns:
            bool -- A boolean representing if a multi-data handler exists.
        """
        self.mult_handler = self.multi.pick(universe)
        if not bool(self.mult_handler):
            # Would return true even if
            return False
        return True
    
    def validate_asset_num(self):
        ids = self.mult_handler.source_ids
        if len(ids) > 0:
            return True
        return False

    def process(self, item:ADict):
        """Given an id inside of the item dictionary `backtest`, get information using that id

            We're expecting a dynamic `universe` key inside of the dictionary.

        Arguments:
            item {ADict} -- Addict modified dictionary. Saved according to backtest data.

        Returns:
            ADict -- Modified dictionary with action and percentage inside of it
        """
        universe_id:str = item.config.universe
        if not self.settings.override:
            is_multi = self.check_multi(universe_id)
            if is_multi:
                if self.validate_asset_num():
                    item.valid_multi=True
                    item.failed = False
                    item.msg = "Successfully confirmed the Universe is valid"
                    item.asset_metadata = self.mult_handler.source_ids
                    return item
            item.valid_multi=False
            item.failed = True
            item.msg = "Universe was not valid"
            item.asset_metadata = []
            return item
        
        item.valid_multi=True
        item.msg = "Universe was not valid"
        item.asset_metadata = []
        return item

    # @logger.catch(reraise=True)
    def step(self, item:ADict, **settings):
        return super().step(item, **settings)