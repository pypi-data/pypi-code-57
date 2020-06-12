import uuid
import maya
import random
from cytoolz.curried import pipe, map, filter, get
from cytoolz.itertoolz import unique

from typing import Optional, List
from jamboree import Jamboree
from jamboree.base.processors.abstracts import Processor
from jamboree.handlers.abstracted.search import ParameterizedSearch
from jamboree.handlers.default.search import BaseSearchHandler
from see137.search.prototype import SearchFacade
from loguru import logger

class _BacktestUniverseManagement(BaseSearchHandler):
    """ 
        # Changing this method to store all relavent universe information.

        Things like descriptions, userid, name, extra tags. Use to optimize query to a single component when reading.
        
        
        ```
    """
    def __init__(self):
        super().__init__()
        self.entity = "universe_information"
        # actually, let's say the multi-id and universe id are separate 
        self.dreq = {"universe": str, "name": str, "description": str, "user":str, "tags":list}

class BacktestUniverseManagement(SearchFacade):
    def __init__(self):
        super().__init__(_BacktestUniverseManagement)


class UniverseCreate(BacktestUniverseManagement):
    """ 
        Used to find stategies and universes by asset or universe. 

        Store all relavent information regarding the user/universe interaction. Use to denormalize

        ```py
            # Match a strategy with a universe and asset
            backtest_manager.create.universe.init(universe: str, strategy: str, asset:str)
        ```
    """
    def __init__(self):
        super().__init__()
        self.must_have = ["universe"]
    
    def init(self, universe: str, name:str, user:str, description:str, tags:List[str]=[]):
        if bool(tags):
            universe_mix_id = self.Create(no_overwrite_reqs=True, universe=universe, name=name, user=user, description=description, tags=tags)
        return universe_mix_id

    
    
class UniverseUpdate(BacktestUniverseManagement):
    """ 
        Use to find backtest information by episodes, and episodes by backtest

        ```py
            # Start a new backtest
            backtest_manager.create.universe.init(backtest_id)

            
        ```
    """
    def __init__(self):
        super().__init__()
        
    
    def name(self, universe:str, _name:str):
        """ Update episode status """
        self.UpdateID(universe, name=_name)
    
    def description(self, universe:str, description:str):
        self.UpdateID(universe, description=description)
    

        

    


class UniverseInfo(BacktestUniverseManagement):
    """ 
        Use to find backtest information by episodes, and episodes by backtest

        - Is there any backtest that's running right now?
        - Find all of the unique universes

        ```py
            # Get the difference
            backtest_manager.info.episodes.by_backtest(backtest_id)
            
        ```
    """
    def __init__(self):
        super().__init__()
    
    @property
    def universes(self) -> List[dict]:
        """ get all episodes """
        universes = self.Find("*")
        unis = pipe(universes, map(lambda uni: uni['universe']), unique, list)
        return unis
    
    @property
    def assets(self) -> List[dict]:
        """ Get all active episodes"""
        assets = self.Find("*")
        unis = pipe(assets, map(lambda uni: uni['asset']), unique, list)
        return unis
    
    @property
    def strategies(self) -> List[str]:
        """ Return a list of list of strategy IDs"""
        strategies = self.Find("*")
        unis = pipe(strategies, map(lambda uni: uni['strategy']), unique, list)
        return unis



    @property
    def total_universes(self) -> int:
        return len(self.universes)

    @property
    def total_strategies(self) -> int:
        return len(self.strategies)
    
    @property
    def total_assets(self) -> int:
        return len(self.assets)

    
    def universes_by_user(self, user:str):
        """ Get all of the created universes by user. """
        strategy_list = self.Find(user=user)
        strats = pipe(strategy_list, map(lambda uni: uni['universe']), unique, list)
        return strats
    
    def by_user(self, user:str):
        """ Get all records by user."""
        strategy_list = self.Find(user=user)
        return strategy_list

    
    def asset_by_universe(self, universe:str):
        assets = self.Find(universe=universe)
        _assets = pipe(assets, map(lambda assss: assss['asset']), unique, list)
        return _assets
    
    def by_fuzzy_description(self, description:str):
        if bool(description):
            records = self.Find(description=f"{description}*")
            return records
        return []

class UniverseRemove(BacktestUniverseManagement):
    """ 
        
    """
    def __init__(self):
        super().__init__()

    def by_strat_uni(self, strategy:str, universe:str):
        """ Remove episode by id"""
        self.Remove(strategy=strategy, universe=universe)

    def by_strat_asset(self, strategy:str, asset:str):
        self.Remove(strategy=strategy, asset=asset)


def manage_assets():
    strat_id = uuid.uuid4().hex
    universe_ids = [uuid.uuid4().hex for x in range(10)]
    asset_ids = [uuid.uuid4().hex for x in range(200)]
    
    proc = Jamboree()
    universe_create =    UniverseCreate()
    universe_update =    UniverseUpdate()
    universe_info =      UniverseInfo()
    universe_remove =    UniverseRemove()
    
    universe_create.processor = proc
    universe_update.processor = proc
    universe_info.processor = proc
    universe_remove.processor = proc

    # for assetid in asset_ids:
    #     for _ in range(10):
    #         universeid = random.choice(universe_ids)
    #         strat_uni_id = universe_create.init(universeid, strat_id, assetid)
    #     strategies = universe_info.strategy_by_asset(assetid)
    #     for x in strategies:
    #         logger.success(f"Sending command to strategy: {x}. Looking for strategy.") 
    #         logger.debug(assetid)

    #     logger.error(strat_uni_id)
    #     assets = universe_info.asset_by_universe(universeid)
    #     logger.warning(assets)

if __name__ == "__main__":
    manage_assets()