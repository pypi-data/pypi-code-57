"""Backtest Environment

Use environment to control backtests remotely inside of the Kafka Queues.
"""


import uuid

import maya
from addict import Dict as ADict
from faker import Faker
from jamboree import Jamboree
from loguru import logger
import json
from see137.parameters import (Parameter, PortfolioParameter,
                               StrategyParameter, TimeParameter,
                               UniverseParameter, UserParameter)
from see137.parameters.fields import (CurrencyFields, ExchangeFields,
                                      MovementSpecification, TimeRange)
from see137.pipelines.setup_backtest import CreateBacktestPipeline
from see137.search.backtesting import BacktestManager
import requests
logger.disable("jamboree")
# logger.disable("see137")


class BacktestEnvironment:
    def __init__(self,
                 name: str,
                 description: str,
                 time_param: TimeParameter = None,
                 portfolio_param=None,
                 universe_param=None,
                 user_param=None,
                 strategy_param=None):
        self.backtest_identity = None
        self.bid = None

        self.name = name
        self.description = description
        # Search for all backtest

        # Set multi data config
        self.time_param = time_param
        self.portfolio_param = portfolio_param
        self.universe_param = universe_param
        self.user_param = user_param
        self.strategy_param = strategy_param
        self.__pipeline = CreateBacktestPipeline()
        self.verify()

        # Private To Be Called by Property
        self.__backtest_manager = BacktestManager()

    @property
    def processor(self):
        """Processor

        Returns
        -------
        Processor
            The jamboree object that processes everything.

        Raises
        ------
        AttributeError
            Raises when the Jamboree flywheel object doesn't work.
        """
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

    @property
    def pipeline(self):
        """Backtest Pipeline

        Gets the backtest creation pipeline.
        Verification and creation of a backtest to be picked up in the system.

        Returns
        -------
        AddictPipeline
            CreateBacktestPipeline - Backtest creation pipeline.
        """
        self.__pipeline.processor = self.processor
        return self.__pipeline

    def monitor(self):
        """ What we use to aggrgate the information about the backtest."""
        # Once we have an id generated and appended
        return None

    def performance(self):
        """ Get the performance of the backtest """
        return None

    def status(self):
        """ Get the current status of the backtest. Is it finished? How much time left?"""
        return None

    def resources(self):
        return None

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
        """Verify
        Verifies that all of the parameters are available.

        Raises
        ------
        AttributeError
            One of the attributes is missing.
        TypeError
            One of the attributes isn't a parameter system.
        """
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
            BacktestEnvironment -- return a valid instance of the backtest environment we're looking for.
        """
        return None
        # return BacktestEnvironment

    def create(self):
        extract = self.extract()
        backtest_info = ADict()
        backtest_info.config = extract
        _info = self.pipeline.step(backtest_info)
        is_success = (not _info.failed)
        message = str(_info.msg)
        backtestid = str(_info.backtestid)

        if not is_success:
            raise Exception(message)
        
        # Set the backtestid to be used elsewhere
        self.bid = backtestid

    def connect(self):
        """ Input settings of a place to send the start command to remote service"""
        try:
            response = requests.get("http://localhost:6066/episodes/connect")
            logger.warning(response.status_code)
            response.json()
            return True
        except json.decoder.JSONDecodeError:
            logger.error("FAILED CONNECTION")
            return False
        except Exception as exe:
            # Using a catch all for some otehr error that might pop up
            logger.exception(exe)
            return False
        

    def push(self):
        try:
            response = requests.post("http://localhost:6066/episodes/init", json={"backtest": self.bid})
            jresponse = response.json()
            is_successful = jresponse.get("success", False)
            if not is_successful:
                return False
            logger.success(f"Backtest = {self.bid} was successfully started")
            return True
        except json.decoder.JSONDecodeError:
            return False
        except Exception:
            return False

    @logger.catch(reraise=True)
    def start(self):
        if self.connect():
            self.create()
            self.push()


def main():
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
