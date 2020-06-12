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

class ProcedureSearch(BaseSearchHandler):
    def __init__(self):
        super().__init__()
        self.entity = "asset_complex"
        self.dreq = {"typing":str, "asset": str, "params": dict, "next_delta": float, "interval": float}

class UniverseAssetCreate(SearchFacade):
    """ 
        Used to find stategies and universes by asset or universe. 

        - Get the 

        ```py
            # Match a strategy with a universe and asset
            backtest_manager.create.universe_asset.init(universe: str, asset:str)
        ```
    """
    def __init__(self):
        super().__init__(ProcedureSearch)
    
    def init(self, universe: str, asset:str):
        universe_mix_id = self.Create(no_overwrite_reqs=True, universe=universe, asset=asset)
        return universe_mix_id

    
    
class UniverseAssetUpdate(SearchFacade):
    def __init__(self):
        super().__init__(ProcedureSearch)
        

    


class UniverseAssetInfo(SearchFacade):
    def __init__(self):
        super().__init__(ProcedureSearch)
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
    def total_universes(self) -> int:
        return len(self.universes)


    
    @property
    def total_assets(self) -> int:
        return len(self.assets)

    
    def universes_by_asset(self, assetid:str):
        """ Get all strategies by asset ID """
        strategy_list = self.Find(asset=assetid)
        strats = pipe(strategy_list, map(lambda uni: uni['universe']), unique, list)
        return strats
        

    
    def asset_by_universe(self, universe:str):
        assets = self.Find(universe=universe)
        _assets = pipe(assets, map(lambda assss: assss['asset']), unique, list)
        return _assets

class UniverseAssetsRemove(SearchFacade):
    """ 
        
    """
    def __init__(self):
        super().__init__(ProcedureSearch)
    

    def by_universe(self, universe:str):
        """ Remove episode by id"""
        self.Remove(universe=universe)

    def by_asset(self, asset:str):
        self.Remove(asset=asset)


def manage_assets():
    pass
    # universe_id = uuid.uuid4().hex
    # asset_ids = [uuid.uuid4().hex for x in range(200)]
    
    # proc = Jamboree()
    # universe_create =    UniverseAssetCreate()
    # universe_update =    UniverseAssetUpdate()
    # universe_info =      UniverseAssetInfo()
    # universe_remove =    UniverseAssetsRemove()
    
    # universe_create.processor = proc

    # universe_update.processor = proc
    # universe_info.processor = proc
    # universe_remove.processor = proc
    # universe_remove.All()
    # for assetid in asset_ids:
    #     universe_create.init(universe_id, assetid)
    #     logger.warning(universe_info.assets)
    #     logger.success(universe_info.universes)

if __name__ == "__main__":
    manage_assets()