import random
import uuid
import time
import maya
import pandas as pd
import requests
from crayons import cyan, magenta
from jamboree import Jamboree
from loguru import logger

from see137.config.fields import StepField
from see137.handlers.strategy.core import StrategyEngine
from see137.search.backtesting import BacktestManager


class SampleStrategy(object):
    def step(self, df: pd.DataFrame):
        return random.choice([0, 1, 2])


class ProblemSetup:
    def __init__(self):
        self.name = "Test Strategy"
        self.description = "Test Description"
        self.user_id = uuid.uuid4().hex
        self.processor = Jamboree()
        # self.must_have = ['name', 'description', 'userid']
        self.url = "http://localhost:6066"
        self.manager = BacktestManager()
        self.manager.processor = self.processor
        self.backtest_id: str = ""
        self.strategy_id: str = ""
        self.strategy = StrategyEngine(processor=self.processor)
        self.cash = 10000.0
        """ 
            name="SAMPLE_NAME",
            category="SAMCATSASS",
            subcategories={"sam": "ple"},
            submetatype="OTHER SMAPLE",
            abbreviation="SAP",
        """

    def create_backtest(self):
        self.backtest_id = self.manager.create.backtest.init(
            name=self.name, description=self.description, userid=self.user_id)
        # self.current_strategy_engine
        logger.info(
            f"Create backtest config in DB: {magenta(self.backtest_id)}")
    def save_strategy_getmeata(self):
        """ Save strategy and get metadata"""
        self.strategy['name'] = "SAMPLE_NAME"
        self.strategy['subcategories'] = {"sam": "ple"}
        self.strategy['category'] = "SAMCATSASS"
        self.strategy['submetatype'] = "OTHER SMAPLE"
        self.strategy['abbreviation'] = "SAP"
        self.strategy.blobfile = SampleStrategy()
        self.strategy.reset()
        self.strategy_id = str(self.strategy.metaid)

    def update_strategyid(self):
        self.manager.update.backtest.UpdateID(self.backtest_id,
                                              strategy=self.strategy_id)
        btest = self.manager.info.backtest.FindById(self.backtest_id)

        vals = list(btest.values())
        logger.warning(self.strategy_id)
        logger.info(
            f"Saving strategy and getting the metadata id associated with it {cyan(btest['name'], bold=True)}"
        )
        logger.error(random.choice(vals))
        current_strategy = self.strategy.pick(btest['strategy'])
        with current_strategy as srt:
            logger.success(f"Strategy action will be: {srt.step(123)}")

    def setup_time(self):
        start_time = maya.when("2007-05-02")
        end_time = maya.when("2020-04-19")
        step_information = StepField()
        step_information.hours = 4
        logger.info(start_time)
        logger.success(end_time)
        logger.warning(step_information.to_epoch())

        self.manager.update.backtest.UpdateID(
            self.backtest_id,
            start_epoch=start_time._epoch,
            end_epoch=end_time._epoch,
            step_size=step_information.to_epoch()
        )

    def setup_portfolio(self):
        self.manager.update.backtest.UpdateID(self.backtest_id,
                                              exchange="binance", start_cash=self.cash)
        btest = self.manager.info.backtest.FindById(self.backtest_id)
        logger.warning(type(btest['exchange']))

    def create_universe(self):
        """ Moving this to another script file"""
        pass

    def add_assets_to_universe(self):
        """ Moving this to another script file. """
        pass

    def add_universe(self):
        """ Add a universe of assets """
        logger.info("add a universe of assets")
        self.manager.update.backtest.UpdateID(self.backtest_id,
                                              universe=uuid.uuid4().hex)
        btest = self.manager.info.backtest.FindById(self.backtest_id)
        logger.warning(btest)

    def send_start_command(self):
        response = requests.post(f"{self.url}/episodes/init",
                                 json={"episode_number": 2, "backtest_id": self.backtest_id})
        logger.info(response.json())

    def start(self):
        self.create_backtest()
        self.save_strategy_getmeata()
        self.update_strategyid()
        self.setup_time()
        self.setup_portfolio()
        self.add_universe()
        self.send_start_command()
        time.sleep(0.01)

# Send an HTTP Request to Faust and work backwards.

# 1. Send HTTP request
# 2. Configure searchable item for backtest
# 3. Pull searchable item from HTTP request
# 4. Create an episode upon request from searchable item pulled
# 5. 
if __name__ == "__main__":
    ProblemSetup().start()
