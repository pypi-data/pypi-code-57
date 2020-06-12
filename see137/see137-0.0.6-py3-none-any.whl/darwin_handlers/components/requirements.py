import datetime as dt
import random
import time
import uuid
from typing import Dict, List

from addict import Dict as ADict
from jamboree import Jamboree
from jamboree.handlers.default.multi import MultiDataManagement
from jamboree.handlers.default.search import BaseSearchHandler
from loguru import logger

from see137 import PortfolioHandler, RequirementsHandler
from see137.common import (AddictPipeline, AddictWithManagerComponent,
                                    ComponentAbstract, Pipeline, PipelineA)
from see137.components.backtest import CreateBacktestComponent
from see137.components.strategy import CheckStrategy
from see137.components.universe import CheckUniverse
from see137.handlers.strategy.core import StrategyEngine
from see137.models.backtests_models import BacktestConfig
from see137.search.prototype import SearchFacade
from see137.search.backtesting.topics.specifics import BacktestEpisodeSpec


class CreateRequirements(AddictWithManagerComponent):
    def __init__(self):
        super().__init__()
        # Backtest configuration dict. Can be saved into the database immediately.
        self.required_items: Dict[str, type] = {"config": dict}
        self.__private_multi = MultiDataManagement()
        self.__private_requirements = RequirementsHandler()
        self.mult_handler = None

    @property
    def requirements(self):
        self.__private_requirements.processor = self.processor
        self.__private_requirements.live = False
        return self.__private_requirements

    def check_prev(self, item):
        return super().check_prev(item)

    def check_all(self, item):
        return super().check_all(item)

    def check_item(self, item):
        return super().check_item(item)

    @property
    def multi(self):
        self.__private_multi.processor = self.processor
        return self.__private_multi

    def process(self, item: ADict):
        """Steps:

            1. Pull universe
            2. Verify it

        Arguments:
            item {ADict} -- Addict modified dictionary. Save's according to backtest data.

        Returns:
            ADict -- Modified dictionary with action and percentage inside of it
        """
        universe = item.config.universe
        logger.debug(f"Trying to pull the universe: {universe}")
        universe_handler = self.multi.pick(universe)
        if universe_handler is None:
            raise AttributeError("Universe doesn't exist")

        asset_list = universe_handler.sources
        asset_suc_msg = f"Successfully pulled universe of assets for {universe}"
        logger.success(asset_suc_msg)
        general_req_name = f"general_universe_{universe}"
        item.requirementid = general_req_name
        self.requirements['name'] = general_req_name
        self.requirements.live = False
        self.requirements.reset()
        self.requirements.asset_update(asset_list)
        self.requirements.episode = item.current_episode

        episodic_requirements = self.requirements.unique()
        msg = f"UNIQUE REQUIREMENTS {episodic_requirements}"
        logger.warning(msg)
        return item


class AttachToEpisode(AddictWithManagerComponent):
    """Attaches everything from the prior steps to the episode:

    1. Requirement name
    2. StrategyID
    3. Aggregate Portfolio ID

    Arguments:
        AddictWithManagerComponent {[type]} -- Basically a component that uses addict as a foundation
    """
    def __init__(self):
        super().__init__()
        # Backtest configuration dict. Can be saved into the database immediately.
        self.required_items: Dict[str, type] = {
            "config": dict,
            "requirementid": str,
            "current_episode": str
        }
        self.__private_epispec = BacktestEpisodeSpec()
        self.__private_multi = MultiDataManagement()
        self.__private_requirements = RequirementsHandler()
        self.mult_handler = None

    @property
    def requirements(self):
        self.__private_requirements.processor = self.processor
        self.__private_requirements.live = False
        return self.__private_requirements

    @property
    def spec(self):
        self.__private_epispec.processor = self.processor
        return self.__private_epispec

    def check_prev(self, item):
        return super().check_prev(item)

    def check_all(self, item):
        return super().check_all(item)

    def check_item(self, item):
        return super().check_item(item)

    @property
    def multi(self):
        self.__private_multi.processor = self.processor
        return self.__private_multi

    def process(self, item: ADict):
        """Steps:

            1. Pull universe
            2. Verify it

        Arguments:
            item {ADict} -- Addict modified dictionary. Save's according to backtest data.

        Returns:
            ADict -- Modified dictionary with action and percentage inside of it
        """
        universe = item.config.universe
        strategy = item.config.strategy
        backtest = item.backtestid
        episode = item.current_episode

        save_ref = self.spec.Create(no_overwrite_reqs=True,
                                    universe=universe,
                                    strategy=strategy,
                                    backtest=backtest,
                                    episode=episode)
        logger.error(f"The save reference is: {save_ref}")
        return item

