import uuid
import maya

from typing import Optional, List
from jamboree import Jamboree
from jamboree.base.processors.abstracts import Processor
from jamboree.handlers.abstracted.search import ParameterizedSearch
from jamboree.handlers.default.search import BaseSearchHandler
from see137.search.prototype import SearchFacade
from loguru import logger



class _CoreBacktestSearch(BaseSearchHandler):
    """ 
        # Core Backtest Search  

        Use to find backtesting information.

        Examples:

        ```py

            backtest_manager.create.backtest.init(**kwargs)


            backtest_manager.update.backtest.general(id, **kwargs)
            backtest_manager.update.backtest.time(id, **kwargs)
            backtest_manager.update.backtest.portfolio(id, **kwargs)
            backtest_manager.update.backtest.description(id, **kwargs)
            backtest_manager.update.backtest.strategy(id, **kwargs)


            backtest_manager.info.backtest.by_id(id)
            backtest_manager.info.backtest.by_user(userid)
            backtest_manager.info.backtest.by_exchange(exchange)
            backtest_manager.info.backtest.by_strategy(strategy_id)
            backtest_manager.info.backtest.by_universe(universe_id)

            backtest_manager.info.backtest.start_before('...')
            backtest_manager.info.backtest.start_after('...')
            backtest_manager.info.backtest.start_between(start='...', end='...')

            backtest_manager.info.backtest.end_before('...')
            backtest_manager.info.backtest.end_after('...')
            backtest_manager.info.backtest.end_between(start='...', end='...')


            backtest_manager.remove.backtest.by_user(userid)
            backtest_manager.remove.backtest.by_exchange(exchange)
            backtest_manager.remove.backtest.by_strategy(strategy_id)
            backtest_manager.remove.backtest.by_universe(universe_id)

            backtest_manager.info.backtest.over_cutoff(backtestid, current_time)
        ```
    """

    def __init__(self):
        super().__init__()
        self.entity = "backtest_configuration"
        self.dreq = {
            "user": str,
            "name": str,
            "description": str,

            # Time series information.
            "start": float,
            "end": float,
            "step": str,
            "lookback": str,

            # Outside information
            "base": str,
            "initial": float,

            "exchange": str,

            # Outside information
            "strategy": str,
            "universe": str,
        }

class CoreBacktestSearch(SearchFacade):
    def __init__(self):
        super().__init__(_CoreBacktestSearch())
        self.must_have = ['name', 'description', 'user']
        


class BacktestCreate(CoreBacktestSearch):
    def __init__(self):
        super().__init__()
    
    # @logger.catch
    def init(self, **kwargs):
        backtest_id = self.Create(no_overwrite_reqs=True, **kwargs)
        return backtest_id

    

class BacktestUpdate(CoreBacktestSearch):
    def __init__(self):
        super().__init__()
        self.any_time: List[str] = ["start", "end", "step"]
        self.any_portfolio: List[str] = ["initial", "exchange", "universe"]
        self.any_description: List[str] = ["description"]
        self.any_strategy: List[str] = ["strategy"]
    
    def generalized(self, _id:str, **kwargs):
        self.UpdateID(_id, **kwargs)

    def time(self, _id:str, **kwargs):
        """ Update time information to a backtest. """
        if len(kwargs) == 0:
            return
        if any(anne in kwargs for anne in self.any_time):
            self.UpdateID(_id, **kwargs) #start_epoch

    def portfolio(self, _id:str, **kwargs):
        """ Add portfolio information for a backtest """
        if len(kwargs) == 0:
            return
        if any(anne in kwargs for anne in self.any_portfolio):
            self.UpdateID(_id, **kwargs) #start_epoch


    def strategy(self, _id:str, **kwargs):
        """ Set a strategy """
        if any(anne in kwargs for anne in self.any_strategy):
            self.UpdateID(_id, **kwargs)


class BacktestInfo(CoreBacktestSearch):
    """ 

        backtest_manager.info.backtest.by_id(id)
        backtest_manager.info.backtest.by_user(userid)
        backtest_manager.info.backtest.by_exchange(exchange)
        backtest_manager.info.backtest.by_strategy(strategy_id)
        backtest_manager.info.backtest.by_universe(universe_id)

        backtest_manager.info.backtest.start_before('...')
        backtest_manager.info.backtest.start_after('...')
        backtest_manager.info.backtest.start_between(start='...', end='...')

        backtest_manager.info.backtest.end_before('...')
        backtest_manager.info.backtest.end_after('...')
        backtest_manager.info.backtest.end_between(start='...', end='...')
    """
    def __init__(self):
        super().__init__()
    
    @property
    def count(self) -> int:
        return 0
    
    def generalized(self, term:str=None, **kwargs):
        return self.Find(general=term, **kwargs)

    def by_id(self, _id:str, **kwargs):
        return self.FindById(_id)

    def by_user(self, user:str):
        return self.Find(user=user)

    def by_exchange(self, exchange:str):
        return self.Find(exchange=exchange)

    def by_strategy(self, strategy:str):
        return self.Find(strategy=strategy)

    def by_universe(self, universe:str):
        return self.Find(universe=universe)

    def over_cutoff(self, backtest_id:str, current_time:float):
        backtest_info = self.FindById(backtest_id)
        if not bool(backtest_info):
            return True
        


class BacktestRemove(CoreBacktestSearch):
    def __init__(self):
        super().__init__()
    
    def generalized(self, term:str=None, **kwargs):
        if term is not None:
            self.general = term
        
        self.Remove(**kwargs)

    def by_id(self, _id:str):
        pass

    def by_user(self, user:str):
        return self.Remove(user=user)

    def by_exchange(self, exchange:str):
        return self.Remove(exchange=exchange)

    def by_strategy(self, strategy:str):
        return self.Remove(strategy=strategy)

    def by_universe(self, universe:str):
        return self.Remove(universe=universe)

def manage_episodes():
    from faker import Faker

    Faker.seed(444)


    fake = Faker()
    jampack = Jamboree()
    backtest_create =   BacktestCreate()
    backtest_update =   BacktestUpdate()
    backtest_info =     BacktestInfo()
    backtest_remove =   BacktestRemove()


    backtest_create.processor = jampack
    backtest_update.processor = jampack
    backtest_info.processor = jampack
    backtest_remove.processor = jampack


    while True:
        user_id = uuid.uuid4().hex
        name = f"{fake.first_name()} {fake.last_name()}"
        description = str(fake.sentence())
        backtest_id = backtest_create.init(name=name, description=description, userid=user_id)
        logger.error(description)
        logger.success(backtest_info.by_id(backtest_id).get("description", ""))
        logger.debug(backtest_info.generalized(name=name))


if __name__ == "__main__":
    manage_episodes()