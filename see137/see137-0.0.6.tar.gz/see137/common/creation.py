import copy
import random
import uuid
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

import dask
import maya
from jamboree import Jamboree
from jamboree.handlers.default.data import DataHandler
from loguru import logger

from see137 import PortfolioHandler, RequirementsHandler
from see137.data import PriceGenerator
from see137.utils.trades.trade import DynamicTrade, Trade, TradeType


class SimulationCreator(object):
    """ 
        # Simulation Creator
        ---
        Create a simulation that we'll be able to run through the faust pipeline.

        * Requirements
        * Stochastic Data
        * Portfolios
        * TimeHandler
    """
    def __init__(self,
                 start_balance=10000,
                 session_id: str = uuid.uuid4().hex,
                 ecount=10,
                 exchange="fake_exchange",
                 **kwargs) -> None:
        self.session: str = session_id
        self.episode_count = ecount
        self.exchange = exchange
        self.start_balance = start_balance
        self.assets = [
            "USD_BTC", "USD_ATL", "USD_TRX", "USD_ETH", "USD_BCH", "USD_XRP",
            "USD_EOS", "USD_XTZ", "USD_LINK", "USD_ADA"
        ]

        # Generated hexes
        self.episodes = [uuid.uuid4().hex for i in range(self.episode_count)]
        self.user_id = uuid.uuid4(
        ).hex  # We're generating a fake user id for the time being
        #
        self._current_episode: Optional[str] = None
        self.processor = Jamboree()

        # Kwargs
        self.min_price = kwargs.get("min_price", 200)
        self.max_price = kwargs.get("max_price", 5000)
        self.varied = kwargs.get("is_varied", True)
        self.length = kwargs.get("length", 5000)

        # Blanks
        self.generated = None
        self.is_requirements_reset = False

        self.submetatype = "temporary_price"
        self.abbreviation = "GEN"

    @property
    def current_episode(self) -> str:
        if self._current_episode is None:
            return uuid.uuid4().hex
        return self._current_episode

    @current_episode.setter
    def current_episode(self, _episode: str):
        self._current_episode = _episode

    @property
    def pricing(self):
        data_handler = DataHandler()
        data_handler.processor = self.processor
        data_handler["category"] = self.category
        data_handler["subcategories"] = self.subcategories
        data_handler['submetatype'] = self.submetatype
        data_handler['abbreviation'] = self.abbreviation
        return data_handler

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
            "subcategories": sub,
            "submetatype": self.submetatype,
            "abbreviation": self.abbreviation
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

    @property
    def sampled_portfolio(self):
        """ Return a sample portfolio for the user """
        assest_num = len(self.assets)
        num_sample = random.randint(2, assest_num)
        asset_sample = random.sample(self.assets, num_sample)
        return asset_sample

    @property
    def generator(self):
        """ Price generator """
        price_generator = PriceGenerator()
        price_generator.episodes = self.episodes
        price_generator.assets = self.assets
        price_generator.starting_min = self.min_price
        price_generator.starting_max = self.max_price
        price_generator.is_varied = self.varied
        price_generator.length = self.length
        return price_generator

    @property
    def portfolio(self):
        """ """
        portfolio = PortfolioHandler(start_balance=self.start_balance)
        portfolio.processor     = self.processor
        portfolio['session']    = self.session
        portfolio['exchange']   = self.exchange
        portfolio['user_id']    = self.user_id
        portfolio['episode']    = self.current_episode
        portfolio['live'] = False
        portfolio.reset()
        portfolio.is_sim = True
        portfolio.is_inner_allocation = False
        return portfolio

    @property
    def current_generated(self) -> dict:
        """ Get all of the prices for current episode """
        if self.generated is None:
            self.generator.generate_all_episodes()
        current_prices = self.generated
        return current_prices.get(self.current_episode, {})

    @property
    def requirements(self):
        requirements = RequirementsHandler()
        requirements.processor = self.processor
        requirements['name'] = f"general-{self.session}"
        requirements.episode = self.current_episode
        requirements.live = False
        requirements.reset()
        # if self.is_requirements_reset == False:

        #     self.is_requirements_reset = True
        return requirements

    def generate(self):
        self.generated = self.generator.generate_all_episodes()

        #

    def save_generated(self):
        """ Saving generated data for use in real life """
        logger.info("Saving generated data")
        current_pricing = self.pricing
        current_generated = self.current_generated
        for asset in self.assets:
            current_pricing['name'] = asset
            data = current_generated.get(asset)
            current_pricing.reset()
            current_pricing.store_time_df(data, is_bar=True)

    def load_requirements(self):
        required_items = self.required
        self.requirements.asset_update(required_items)
        # self.requirements.update()

    def load_assets(self):
        """ Loads the user's assets into the portfolio """
        user_sample = self.sampled_portfolio
        current_portfolio = self.portfolio
        for asset in user_sample:
            extras = {
                "submetatype": self.submetatype,
                "abbreviation": self.abbreviation
            }
            current_portfolio.add_asset(asset,
                                        self.subcategories,
                                        extras=extras)
        # logger.info(self.portfolio.pricing.sources)

    def load_unique_requirements(self):
        self.requirements.live = False
        self.requirements.episode = self.current_episode
        self.requirements.unique()
        # logger.info(self.portfolio.pricing.sources)

    def load_allocation(self):
        current_portfolio = copy.copy(self.portfolio)
        current_portfolio.step_price(forced=True)

    def adjust_time(self):
        """
            portfolio_hand.time.head = maya.now().add(weeks=25)._epoch
            portfolio_hand.time.change_stepsize(microseconds=0, days=1, hours=0)
            portfolio_hand.time.change_lookback(microseconds=0, weeks=25, hours=0)
        """

        self.portfolio.time.head = maya.now().add(weeks=5)._epoch
        self.portfolio.time.change_stepsize(microseconds=0, days=1, hours=0)
        self.portfolio.time.change_lookback(microseconds=0, weeks=5, hours=0)
        self.portfolio.pricing.sync()

    def start_debug(self):
        self.load_requirements()

    def start(self):
        """ Create all of the episodes"""
        self.load_requirements()
        self.generate()
        logger.info("Successfully starting session")
        generation_tasks = []
        for episode in self.episodes:
            self.current_episode = episode
            self.save_generated()
            self.adjust_time()
            self.load_assets()
            self.load_allocation()
            self.load_unique_requirements()


def process_rebalance(current_portfolio: PortfolioHandler,
                      current_requirements: RequirementsHandler):
    logger.debug("Stepping forward for the user")
    current_portfolio.time.step()
    current_portfolio.is_inner_allocation = True
    current_portfolio.step_price()
    current_portfolio.is_inner_allocation = False
    logger.error("Finished all assets in episode")


if __name__ == "__main__":
    simulation_creator = SimulationCreator(length=2000, ecount=2)
    simulation_creator.start()
    # executor = ThreadPoolExecutor()

    # Get all of the active assets in the simulation

    while True:
        is_done = False
        for episode in simulation_creator.episodes:
            simulation_creator.current_episode = episode
            current_portfolio = simulation_creator.portfolio
            current_requirements = simulation_creator.requirements.unique()
            active_assets = current_requirements.assets
            current_active = copy.copy(active_assets)
            while True:
                if not current_portfolio.pricing.is_next:
                    is_done = True
                    break

                active = current_active.pop()
                symbol = active.get('name')
                asset_msg = f"Processing the asset: {symbol} for episode: {episode} we'd pull data and process it."
                # logger.info(magenta(asset_msg))
                current_item = simulation_creator.pricing
                current_item['name'] = symbol
                current_item.episode = episode
                current_item.live = False
                current_item.reset()
                # Get the callocation and fill information here
                user_id = current_portfolio.user_id
                # logger.warning(f"User ID is {user_id}")
                current_portfolio.add_asset(symbol)
                current_item.closest_head()
                current_allocation = current_portfolio.current_allocation(symbol=symbol)
                current_limit = current_portfolio.current_pct_limit(symbol=symbol)
                is_not_default = "{:.21f}".format(float(current_allocation)) != '0.000000000000000000001'
                
                # if is_not_default:
                logger.warning((symbol, current_allocation, current_limit, episode))
                # logger.debug(current_limit)
                if current_portfolio.is_user_asset(active):
                    # logger.success(asset_msg)
                    if random.uniform(0, 1) < 0.1:
                        # Makes trade for portfolio
                        trade_type = random.choice([TradeType.LIMIT_BUY, TradeType.LIMIT_SELL])
                        dynamic_trade = DynamicTrade(symbol, trade_type)
                        dynamic_trade.percentage = random.normalvariate(0.3, 0.06)
                        current_portfolio.step(dynamic_trade)
                    else:
                        current_portfolio.step()
                current_requirements.report_cardinality(active)
                if current_requirements.is_valid_cardinality:
                    current_requirements.flush_cardinality()
                    current_portfolio.time.step()

                    logger.error("Next time step in episode")
                    # This should be done elsewhere to prevent locking
                    current_portfolio.step_price(forced=True)
                    break

        if is_done is True:
            break