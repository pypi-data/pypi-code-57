# As a user, I'd like to pull the attached process strategy, pull the data, process the data, get a decision from that data
from addict import Dict as ADict
from typing import List
from jamboree.handlers.default.multi import MultiDataManagement
from see137.handlers.strategy.core import StrategyEngine
from see137.common import Pipeline, ComponentAbstract, AddictWithManagerComponent
from loguru import logger

class CheckStrategy(AddictWithManagerComponent):
    """
        Checks to see if strategy is valid

        
    """
    def __init__(self):
        super(CheckStrategy, self).__init__()

        # Backtest configuration dict. Can be saved into the database immediately.
        

        self.required_items = {
            "config": dict
        }
        
        
        self.__private_strategy = StrategyEngine()
    
    def check_prev(self, item):
        return super().check_prev(item)

    def check_all(self, item):
        return super().check_all(item)
    
    def check_item(self, item):
        return super().check_item(item)

    @property
    def strategy(self):
        self.__private_strategy.processor = self.processor
        return self.__private_strategy

    def check_strat(self, universe:str):
        """Check the if the multi-data handler exists. Should return none if not.  

        Arguments:
            universe {str} -- [description]

        Returns:
            bool -- A boolean representing if a multi-data handler exists.
        """
        try:
            self.strat_handler = self.strategy.pick(universe)
        except AttributeError:
            return False
        return True
    
    def validate_strategy(self):
        """Checks if the stategy blob is loaded into memory

        Returns:
            [type] -- [description]
        """
        if self.strat_handler.current_strategy is not None:
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

        strategy:str = item.config.strategy
        override = self.settings.override
        
        if override:
            item.valid_strategy=True
            item.msg = "Skipping strategy check due to override"
            return item
        is_strat = self.check_strat(strategy)
        if is_strat:
            if self.validate_strategy():
                item.valid_strategy=True
                item.failed = False
                item.msg = "Successfully confirmed the strategy is valid"
                return item
        item.valid_strategy=False
        item.failed = True
        item.msg = "Universe didn't meet criteria [existing, having assets within it]"
        return item
        

    
    def step(self, item:ADict, **settings):
        return super().step(item, **settings)