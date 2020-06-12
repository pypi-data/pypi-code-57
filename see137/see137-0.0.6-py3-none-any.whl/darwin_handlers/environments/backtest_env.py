# As a user, I'd like to pull the attached process strategy, pull the data, process the data, get a decision from that data
import datetime as dt
import random
import time
import uuid
from typing import Dict, List, Optional

import maya
from addict import Dict as ADict
from faker import Faker
from jamboree import Jamboree
from jamboree.handlers.default.multi import MultiDataManagement
from jamboree.handlers.default.search import BaseSearchHandler
from loguru import logger

from see137 import PortfolioHandler, RequirementsHandler
from see137.common import (AddictPipeline, AddictWithManagerComponent,
                                    ComponentAbstract, Pipeline, PipelineA)
from see137.components.backtest import CreateBacktestComponent
from see137.components.portfolio import CreateEpisodePortfolio
from see137.components.requirements import (AttachToEpisode,
                                                     CreateRequirements)
from see137.components.strategy import CheckStrategy
from see137.components.universe import CheckUniverse
from see137.handlers.strategy.core import StrategyEngine
from see137.models.backtests_models import BacktestConfig
from see137.parameters import (Parameter, PortfolioParameter,
                                        StrategyParameter, TimeParameter,
                                        UniverseParameter, UserParameter)
from see137.parameters.fields import (CurrencyFields, ExchangeFields,
                                               MovementSpecification,
                                               TimeRange)
from see137.search.backtesting import BacktestManager
from see137.search.prototype import SearchFacade


class BacktestEnvironment(object):
    """ Use to setup and start a backtest """
    def __init__(self,
                 name: str,
                 description: str,
                 time_param: TimeParameter = None,
                 portfolio_param=None,
                 universe_param=None,
                 user_param=None,
                 strategy_param=None,
                 *args,
                 **kwargs):
        self.backtest_identity = None

        self.name = name
        self.description = description
        # Search for all backtest

        # Set multi data config
        self.time_param = time_param
        self.portfolio_param = portfolio_param
        self.universe_param = universe_param
        self.user_param = user_param
        self.strategy_param = strategy_param

        self.verify()

        # Private To Be Called by Property
        self.__backtest_manager = BacktestManager()

    @property
    def processor(self):
        if self._processor is None:
            raise AttributeError("Injected processor hasn't been set. ")
        return self._processor

    @processor.setter
    def processor(self, _processor):
        self._processor = _processor

    @property
    def manager(self):
        self.__backtest_manager.processor = self.processor
        return self.__backtest_manager

    def monitor(self):
        """ What we use to aggrgate the information about the backtest."""
        # Once we have an id generated and appended
        pass

    def performance(self):
        """ Get the performance of the backtest """
        pass

    def status(self):
        """ Get the current status of the backtest. Is it finished? How much time left?"""
        pass

    def resources(self):
        pass

    def extract(self) -> dict:
        extract_addict = ADict()
        extract_addict.name = self.name
        extract_addict.description = self.description
        extract_addict.user = self.user_param.user

        extract_addict.base = self.portfolio_param.base
        extract_addict.initial = self.portfolio_param.initial
        extract_addict.exchange = self.portfolio_param.exchange

        extract_addict.start = float(self.time_param.start)
        extract_addict.end = float(self.time_param.end)
        extract_addict.step = self.time_param.step
        extract_addict.lookback = self.time_param.lookback

        extract_addict.strategy = self.strategy_param.strategy
        extract_addict.universe = self.universe_param.universe

        return extract_addict.to_dict()

    def verify(self):
        all_conf = [("Time Parameter", self.time_param),
                    ("Portfolio Parameter", self.portfolio_param),
                    ("Universe Parameter", self.universe_param),
                    ("User Parameter", self.user_param),
                    ("Strategy Parameter", self.strategy_param)]
        for index in range(len(all_conf)):
            key, value = all_conf[index]
            if value is None:
                raise AttributeError(
                    f"{key} is missing. Make sure it is not None")
            if not isinstance(value, Parameter):
                raise TypeError(f"{key} needs to be a Parameter class type")

    @staticmethod
    def by_id(_id: str):
        """Get backtest information by id.

        Pulls the information from the database if it exist.

        Example:
        
        ::
            interval = TimeRange(start=start, end=end)
            steps = MovementSpecification(days=3)
            lookback = MovementSpecification(weeks=4)

            time_parameter = TimeParameter(interval=interval,
                                        steps=steps,
                                        lookback=lookback)

            currency = CurrencyFields()
            exchange = ExchangeFields("coinbase")

            portfolio_parameter = PortfolioParameter(currency=currency,
                                                    exchange=exchange)
            user_parameter = UserParameter("userid")
            universe_parameter = UniverseParameter("universeid")
            strategy_parameter = StrategyParameter("strategyid")
            

        Arguments:
            _id {str} -- The id of the backtest we're trying to retrieve. 

        Returns:
            [type] -- [description]
        """
        """
            # 
            
        """
        # return BacktestEnvironment

    def create(self):
        extract = self.extract()
        # Instead of calling the manager directly, we'd likely end up using a facade over a pipeline that has all of the interactions in place
        # That's because we would need to test that the strategy has everything in order before we push it
        logger.info(extract)
        self.backtest_identity = self.manager.create.backtest.init(**extract)

    def connect(self):
        """ Input settings of a place to send the start command to remote service"""
        logger.debug(
            "Checking http connection of remote service. Crashes if it's not there."
        )

    def push(self):
        logger.warning(
            "Pushing the strategy to do a backtest. Will know if backtest has started shortly."
        )

    def start(self):
        self.create()
        self.connect()
        self.push()


def main():
    import uuid
    from pprint import pprint
    # from see137.pipelines.backtests.save import SaveBacktestPipeline
    # Faker.seed(1000)
    # We'd get this information from the user in real life
    fake = Faker()
    name = fake.company()
    description = fake.sentence()
    start = fake.date_between(start_date="-10y")
    end = maya.now().epoch

    interval = TimeRange(start=start, end=end)
    steps = MovementSpecification(days=3)
    lookback = MovementSpecification(weeks=4)

    time_parameter = TimeParameter(interval=interval,
                                   steps=steps,
                                   lookback=lookback)

    currency = CurrencyFields()
    exchange = ExchangeFields("coinbase")
    portfolio_parameter = PortfolioParameter(currency=currency,
                                             exchange=exchange)
    user_parameter = UserParameter(uuid.uuid4().hex)
    universe_parameter = UniverseParameter("92458de9072d46c8be1883745bc24b37")
    strategy_parameter = StrategyParameter("53970e2f7fae4990978b61c8cd0e5b57")
    injectable_processor = Jamboree()
    backtest_env = BacktestEnvironment(name,
                                       description,
                                       time_param=time_parameter,
                                       portfolio_param=portfolio_parameter,
                                       universe_param=universe_parameter,
                                       user_param=user_parameter,
                                       strategy_param=strategy_parameter)
    backtest_env.processor = injectable_processor
    backtest_env.start()


if __name__ == "__main__":
    main()
