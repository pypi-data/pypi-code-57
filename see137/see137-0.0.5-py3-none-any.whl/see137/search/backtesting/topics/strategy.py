import uuid
import maya

from typing import Optional, List
from jamboree import Jamboree
from jamboree.base.processors.abstracts import Processor
from jamboree.handlers.abstracted.search import ParameterizedSearch
from jamboree.handlers.default.search import BaseSearchHandler
from see137.search.prototype import SearchFacade
from loguru import logger

class _BacktestStrategyManagement(ParameterizedSearch):
    """ 
        Use to find backtest information by episodes, and episodes by backtest

        - Is there any backtest that's running right now?
        - Is the episode still running?
        - Update the episode's status
        - Start an episode
        - Get the number of episodes that are running

        ```py
            # Start a new backtest
            backtest_manager.create.episodes.init(backtest_id)

            backtest_manager.update.episodes.status(backtest_id, "...")

            # Get the difference
            backtest_manager.info.episodes.by_backtest(backtest_id)
            backtest_manager.info.episodes.by_episode(episode_id)

            
            # General running episodes
            backtest_manager.info.episodes.total
            backtest_manager.info.episodes.total_active
            backtest_manager.info.episodes.total_inactive



            backtest_manager.info.episodes.active_by(backtest)
            backtest_manager.info.episodes.inactive_by(backtest)
            backtest_manager.info.episodes.is_running(backtest_id, by="backtest")
            backtest_manager.info.episodes.is_running(episode_id, by="episode")

            backtest_manager.info.episodes.status(episode_id, by="episode")
            backtest_manager.info.episodes.status(backtest_id, by="backtest")
        ```
    """
    def __init__(self):
        super().__init__()
        self.entity = "stategy_online"
        self.dreq = {"strategy": str, "broker": str, "user":str, "live": bool}
        

class BacktestStrategyManagement(SearchFacade):
    def __init__(self):
        super().__init__(_BacktestStrategyManagement())
        self.must_have = ['strategy', 'userid', 'broker']
        self.allowed = ["RUNNING", "DONE"]

    # Universal functions that we'll use in other parts

    def active_by(self, backtest_id:str) -> List[dict]:
        """ Get all active backtests by backtest_id"""
        return self.Find(backtest=backtest_id, status="RUNNING")

    def inactive_by(self, backtest_id:str) -> List[dict]:
        """ Get all inactive backtests by backtest_id"""
        return self.Find(backtest=backtest_id, status="DONE")
    
    def total_active_by(self, backtest_id:str) -> int:
        return len(self.active_by(backtest_id))

    def total_inactive_by(self, backtest_id:str) -> int:
        return len(self.inactive_by(backtest_id))


class StrategyCreate(BacktestStrategyManagement):
    """ 
        Use to find backtest information by episodes, and episodes by backtest

        - Is there any backtest that's running right now?
        - Is the episode still running?
        - Update the episode's status
        - Start an episode
        - Get the number of episodes that are running

        ```py
            # Start a new backtest
            backtest_manager.create.episodes.init(backtest_id)
        ```
    """
    def __init__(self):
        super().__init__()
    
    def init(self, strategy_metadata_id:str, userid:str, broker:str, live:bool=False):
        strategy_id = self.Create(no_overwrite_reqs=True, strategy=strategy_metadata_id, broker=broker, live=live, userid=userid)
        return strategy_id
    
    
class StrategyUpdate(BacktestStrategyManagement):
    """ 
        Use to find backtest information by episodes, and episodes by backtest

        - Is there any backtest that's running right now?

        ```py
            # Start a new backtest

            backtest_manager.update.strategy.status(strategyid, "LIVE")
        ```
    """
    def __init__(self):
        super().__init__()
        
    
    def status(self, episode_id:str, status="RUNNING"):
        """ Update episode status """
        self.UpdateMany({"episode": episode_id}, status="DONE")
        

    


class StrategyInfo(BacktestStrategyManagement):
    """ 
        Use to find backtest information by episodes, and episodes by backtest

        - Is there any backtest that's running right now?
        - Is the episode still running?
        - Update the episode's status
        - Start an episode
        - Get the number of episodes that are running

        ```py
            # Get the difference
            backtest_manager.info.episodes.by_backtest(backtest_id)
            backtest_manager.info.episodes.by_episode(episode_id)

            
            # General running episodes
            backtest_manager.info.episodes.total
            backtest_manager.info.episodes.total_active
            backtest_manager.info.episodes.total_inactive

            # Get active episodes
            # Check if they're running
            backtest_manager.info.episodes.active_by(backtest)
            backtest_manager.info.episodes.inactive_by(backtest)
            backtest_manager.info.episodes.is_running(backtest_id, by="backtest")
            backtest_manager.info.episodes.is_running(episode_id, by="episode")

            backtest_manager.info.episodes.status(episode_id, by="episode")
            backtest_manager.info.episodes.status(backtest_id, by="backtest")
        ```
    """
    def __init__(self):
        super().__init__()
    
    def strategy_by_asset(self, asset_id:str):
        """ Get the strategy by asset """
        assets = self.Find(asset=asset_id)

class StrategyRemove(BacktestStrategyManagement):
    """ 
        
    """
    def __init__(self):
        super().__init__()

    def by_id(self, episode_id:str):
        """ Remove episode by id"""
        self.Remove(episode=episode_id)

    def by_backtest(self, backtest_id:str):
        self.Remove(backtest=backtest_id)


def manage_episodes():
    proc = Jamboree()
    # episode_create = CoreEpisodeCreate()
    # episode_update = CoreEpisodeUpdate()
    # episode_info = CoreEpisodeInfo()
    # episode_remove = CoreEpisodeRemove()


    # episode_create.processor = proc
    # episode_update.processor = proc
    # episode_info.processor = proc
    # episode_remove.processor = proc

    # backtest_id = "3e667a9ade4c4a409ae153522f46cc3d"

    # backtest_id, episode_id, is_running = episode_create.init(backtest_id)
    # print(episode_info.total_active)
    # print(episode_info.status(episode_id))
    # print(episode_info.is_running(episode_id))
    # episode_update.status(episode_update, status="DONE")
    # print(episode_info.status(episode_id))
    # print(episode_info.total_active)
    # print(episode_info.total_inactive)
    # print(episode_info.total_active_by(backtest_id))
    # episode_remove.by_id(episode_id)
    # print(episode_info.total_inactive)

if __name__ == "__main__":
    manage_episodes()