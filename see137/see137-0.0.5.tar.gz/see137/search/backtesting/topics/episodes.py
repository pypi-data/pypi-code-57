import uuid
from typing import List, Optional

import maya
from cytoolz.curried import filter, get, map, pipe
from cytoolz.itertoolz import unique
from jamboree import Jamboree
from jamboree.base.processors.abstracts import Processor
from jamboree.handlers.abstracted.search import ParameterizedSearch
from jamboree.handlers.default.search import BaseSearchHandler
from see137.search.prototype import SearchFacade
from loguru import logger
from pydantic import PositiveInt, ValidationError, validate_arguments



class _BacktestEpisodeStatus(BaseSearchHandler):
    """ 
        Use to find backtest information by episodes, and episodes by backtest

        - Is there any backtest that's running right now?
        - Is the episode still running?
        - Update the episode's status
        - Start an episode
        - Get the number of episodes that are running
        - What is the strategy we're using for this episode?
        - What are the requirements for this episode?
            - Used so we can pull requirements for the episode 

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
        
        self.entity = "episode_backtest_status"
        self.dreq = {"episode": str, "backtest": str, "status":str, 'portfolio':str, "requirements":str, 'strategy':str}
        

class BacktestEpisodeStatus(SearchFacade):
    def __init__(self):
        ProcedureSearch = _BacktestEpisodeStatus()
        super().__init__(ProcedureSearch)
        self.must_have = ['episode', 'backtest']
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


class EpisodeCreate(BacktestEpisodeStatus):
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
    
    def by_backtest(self, backtest_id):
        """ All episodes by backtestid"""
        return self.Find(backtest=backtest_id)

    def init(self, backtest_id:str, **kwargs):
        # logger.bind()
        active_count = self.total_active_by(backtest_id)
        

        
        if active_count == 0:
            episode_id = uuid.uuid4().hex
            _backtest_id = self.Create(no_overwrite_reqs=True, episode=episode_id, backtest=backtest_id, status="RUNNING", **kwargs)
            active_count = self.total_active_by(backtest_id)
            
            return _backtest_id, episode_id, True

        # backtest_id = self.Create(no_overwrite_reqs=True, episode=episode_id, backtest=backtest_id, status="RUNNING", **kwargs)
        
        return backtest_id, None, False
    
    # def init_portfolio()

    
    
class EpisodeUpdate(BacktestEpisodeStatus):
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
        
    
    def status(self, episode_id:str, _status="RUNNING"):
        """ Update episode status """
        if _status not in self.allowed:
            raise ValueError("Episode status must be RUNNING or DONE")
        self.UpdateMany({"episode": episode_id}, status=_status)
    
    
    def strategy(self, episode:str, strategy:str):
        self.UpdateMany({"episode": episode}, status="DONE")
    
    def portfolio(self, episode:str, portfolio:str):
        self.UpdateMany({"episode": episode}, portfolio=portfolio)
    
    def requirements(self, episode:str, requirements:str):
        self.UpdateMany({"episode": episode}, requirements=requirements)
    


class EpisodeInfo(BacktestEpisodeStatus):
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
        self.allowed = ["backtest", "episode"]
    
    @property
    def episodes(self) -> List[dict]:
        """ get all episodes """
        universes = self.Find("*")
        unis = pipe(universes, map(lambda uni: uni['episode']), unique, list)
        return unis
    
    @property
    def active(self) -> List[dict]:
        """ Get all active episodes"""
        return self.Find(status="RUNNING")
    
    @property
    def inactive(self) -> List[dict]:
        """ Get all inactive episodes"""
        return self.Find(status="DONE")

    @property
    def total(self) -> int:
        return len(self.episodes)

    @property
    def total_active(self) -> int:
        return len(self.active)
    
    @property
    def total_inactive(self) -> int:
        return len(self.inactive)

    
    def is_running(self, episode_id:str):
        single_episdoe = self.Find(episode=episode_id, status="RUNNING")
        if len(single_episdoe) > 0:
            return True
        return False
        

    def status(self, episode_id:str):
        single_episode = self.Find(episode=episode_id)
        if len(single_episode) > 0:
            return single_episode[0].get("status")
        return "DONE"

    def by_backtest(self, backtest_id):
        """ All episodes by backtestid"""
        return self.Find(backtest=backtest_id)
    
    def by_episode(self, episode_id:str):
        """ All episodes by backtestid"""
        _episode = self.Find(episode=episode_id)
        if len(_episode) > 0:
            return _episode[0]
        return {}

class EpisodeRemove(BacktestEpisodeStatus):
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
    episode_create = EpisodeCreate()
    episode_update = EpisodeUpdate()
    episode_info = EpisodeInfo()
    episode_remove = EpisodeRemove()


    episode_create.processor = proc
    episode_update.processor = proc
    episode_info.processor = proc
    episode_remove.processor = proc

    backtest_id = "3e667a9ade4c4a409ae153522f46cc3d"
    # episode_remove.general = "*"
    # episode_remove.remove()
    episode_remove.RemoveAll()
    backtest_id, episode_id, is_running = episode_create.init(backtest_id)
    print(episode_info.total_active)
    print(episode_info.status(episode_id))
    print(episode_info.is_running(episode_id))
    episode_update.status(episode_update, _status="DONE")
    print(episode_info.status(episode_id))
    print(episode_info.total_active)
    print(episode_info.total_inactive)
    print(episode_info.total_active_by(backtest_id))
    episode_remove.by_id(episode_id)
    print(episode_info.total_inactive)

if __name__ == "__main__":
    manage_episodes()
