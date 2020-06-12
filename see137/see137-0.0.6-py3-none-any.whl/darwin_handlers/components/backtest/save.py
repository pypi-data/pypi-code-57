# As a user, I'd like to pull the attached process strategy, pull the data, process the data, get a decision from that data
from typing import Dict, List

from addict import Dict as ADict
from jamboree import Jamboree
from jamboree.handlers.default.multi import MultiDataManagement
from loguru import logger

from see137.common import (AddictWithManagerComponent,
                                    ComponentAbstract, Pipeline, PipelineA)
from see137.components.strategy import CheckStrategy
from see137.components.universe import CheckUniverse
from see137.handlers.strategy.core import StrategyEngine
from see137.models.backtests_models import BacktestConfig

class CreateBacktestComponent(AddictWithManagerComponent):
    """Save Backtest Component

        Pull strategy from the database to do work on.
    """
    def __init__(self):
        super(CreateBacktestComponent, self).__init__()


        # Backtest configuration dict. Can be saved into the database immediately.
        self.required_items: Dict[str, type] = {
            "config": dict, "valid_multi":bool, 'valid_strategy':bool
        }

    def check_prev(self, item):
        return super().check_prev(item)

    def check_all(self, item):
        return super().check_all(item)
    
    def check_item(self, item):
        return super().check_item(item)

    def add_backtest_info(self, item: ADict, _id: str, is_save: bool = False):
        item.backtest_id = _id
        item.is_saved = False
        return item

    def process(self, item: ADict):
        """Take the backtest_config and save it into the database.

        Arguments:
            item {ADict} -- Addict modified dictionary. Save's according to backtest data.

        Returns:
            ADict -- Modified dictionary with action and percentage inside of it
        """

        backtestid = self.manager.create.backtest.init(**item.config.to_dict())
        item.backtestid = backtestid
        logger.error(backtestid)
        return item
