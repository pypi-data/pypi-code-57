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
from see137.search.backtesting.topics.portfolio import BacktestPortfolioAgg

class CreateEpisodePortfolio(AddictWithManagerComponent):
    def __init__(self):
        super(CreateEpisodePortfolio, self).__init__()
        # Backtest configuration dict. Can be saved into the database immediately.
        self.required_items: Dict[str, type] = {
            "config": dict,
            "valid_multi": bool,
            'valid_strategy': bool,
            'backtestid': str
        }

    def add_backtest_info(self, item: ADict, _id: str, is_save: bool = False):
        item.backtest_id = _id
        item.is_saved = False
        return item

    # def check_prev()

    def process(self, item: ADict):
        """Take the backtest_config and save it into the database.

        Arguments:
            item {ADict} -- Addict modified dictionary. Save's according to backtest data.

        Returns:
            ADict -- Modified dictionary with action and percentage inside of it
        """
        _, episodeid, is_created = (self.manager.create.episodes.init(
            item.backtestid, strategy=item.config.strategy))
        if is_created == True:
            portfolio_agg = BacktestPortfolioAgg()
            portfolio_agg.processor = self.processor
            aggregationid = (portfolio_agg.Create(
                no_overwrite_reqs=True,
                timestamp=item.config.start,
                episode=episodeid,
                user=item.config.user,
                total=item.config.initial,
                allocation={item.config.base: 1.0},
                performance=item.config.initial))
            agg_msg = f"Aggregate portfolio information ID {aggregationid}"
            logger.success(agg_msg)
            # logger.debug(aggregationid)
            self.manager.update.episodes.portfolio(episodeid, aggregationid)
            _data = self.manager.info.episodes.by_episode(episodeid)
            item.current_episode = episodeid
            item.failed = False
            item.msg = "Backtest was started"
            return item
        elif not bool(episodeid):
            item.current_episode = episodeid
            item.failed = True
            item.msg = "Backtest couldn't be found"
            return item
        item.current_episode = episodeid
        item.failed = True
        item.msg = "Episode already started"
        return item

