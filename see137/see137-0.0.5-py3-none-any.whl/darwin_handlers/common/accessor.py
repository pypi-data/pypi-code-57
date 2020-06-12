import copy
import random
import uuid
from typing import Optional

import maya
from jamboree import JamboreeNew as Jamboree
from jamboree.handlers.default.data import DataHandler
from loguru import logger

from see137 import PortfolioHandler, RequirementsHandler
from see137.data import PriceGenerator


class SingleAccessor(object):
    """ 
        # Simulation Creator
        ---
        Create a simulation that we'll be able to run through the faust pipeline.

        * Requirements
        * Stochastic Data
        * Portfolios
        * TimeHandler
    """
    def __init__(self, start_balance=10000, session_id:str=uuid.uuid4().hex, ecount=10, exchange="fake_exchange", **kwargs) -> None:
        self.session:str = session_id
        self.episode_count = ecount
        self.exchange = exchange
        self.start_balance = start_balance
        self.assets = ["USD_BTC", "USD_ATL", "USD_TRX", "USD_ETH", "USD_BCH", "USD_XRP", "USD_EOS", "USD_XTZ", "USD_LINK", "USD_ADA"]
        
        
        # Generated hexes
        self.episodes = [uuid.uuid4().hex for i in range(self.episode_count)]
        self.user_id = uuid.uuid4().hex # We're generating a fake user id for the time being
        # 
        self._current_episode:Optional[str] = None
        self.processor = Jamboree()
        
        # Kwargs
        self.min_price = kwargs.get("min_price", 200)
        self.max_price = kwargs.get("max_price", 5000)
        self.varied = kwargs.get("is_varied", True)
        self.length = kwargs.get("length", 5000)


        # Blanks
        self.generated = None
    
    def load_first_objects(self):
        self._portfolio = PortfolioHandler()
        self._portfolio = self.processor
        self._requirements = RequirementsHandler()
        self._requirements.processor = self.processor
        self._data = DataHandler()
        self._data.processor = self.processor

    @property
    def portfolio(self):
        """ """
        portfolio = self._portfolio
        portfolio['session'] = self.session
        portfolio['exchange'] = self.exchange
        portfolio['user_id'] = self.user_id
        portfolio['episode'] = self.current_episode
        portfolio['live'] = False
        portfolio.reset()
        return portfolio

    @property
    def requirements(self):
        requirements = self._requirements
        requirements['name'] = f"general-{self.session}"
        requirements.episode = self.current_episode
        requirements.live = False
        requirements.reset()
        return requirements
    
    @property
    def pricing(self):
        data_handler = self._data
        data_handler.processor = self.processor
        data_handler["category"] = self.category
        data_handler["subcategories"] = self.subcategories
        
        return data_handler
    
    @property
    def current_episode(self) -> str:
        if self._current_episode is None:
            return uuid.uuid4().hex
        return self._current_episode

    @current_episode.setter
    def current_episode(self, _episode:str):
        self._current_episode = _episode

    
    
    @property
    def category(self):
        return "markets"
    
    @property
    def subcategories(self):
        return {
            "market": "stock",
            "country": "US",
            "sector": "faaaaake",
            "episode": self.current_episode
        }

    @property
    def required(self):
        sub = self.subcategories
        sub.pop("episode")
        base = {
            "category": self.category,
            "subcategories": sub
        }
        ret_items = []
        for asset in self.assets:
            base = copy.copy(base)
            base['name'] = asset
            ret_items.append(base)
        return ret_items
    
    @property
    def active(self):
        """ Get all of the active requirements"""
        return self.requirements.assets

            
        


if __name__ == "__main__":
    pass
    # simulation_creator = SimulationCreator(length=2000, ecount=1)
    # simulation_creator.start_debug()

    # # Get all of the active assets in the simulation
    # active_assets = simulation_creator.active
    
    # current_active = copy.copy(active_assets)
    # random.shuffle(current_active)

    # while True:
    #     current_asset = current_active.pop()
    #     simulation_creator.requirements.report(current_asset)
    #     # with simulation_creator.requirements.lock():
    #     if simulation_creator.requirements.is_valid:
    #         logger.debug(f"All assets finished. Starting next step {current_asset}")
    #         simulation_creator.requirements.reset_reports()
            
    #         current_active = copy.copy(active_assets)
    #         random.shuffle(current_active)

    #     else:
    #         logger.error(f"Asset: {current_asset}")