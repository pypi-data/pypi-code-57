# As a user, I'd like to pull the attached process strategy, pull the data, process the data, get a decision from that data
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
from see137.components.portfolio import CreateEpisodePortfolio
from see137.components.requirements import (AttachToEpisode,
                                                     CreateRequirements)
from see137.components.strategy import CheckStrategy
from see137.components.universe import CheckUniverse
from see137.handlers.strategy.core import StrategyEngine
from see137.models.backtests_models import BacktestConfig
from see137.search.prototype import SearchFacade

logger.disable('jamboree')
logger.disable(__name__)


def create_backtest_config():
    default_backtest = BacktestConfig()
    default_backtest.universe = "92458de9072d46c8be1883745bc24b37"
    default_backtest.strategy = "53970e2f7fae4990978b61c8cd0e5b57"
    backtest_config = ADict()
    backtest_config.config = default_backtest.dict()
    backtest_config.failed = False
    backtest_config.msg = "Currently starting backtest"
    return backtest_config



def main():
    """
        Functional Pipeline
    """
    processor = Jamboree()

    # EpisodeSpecificInformation()

    create_backtest = AddictPipeline(name="CreateBacktest",
                                     processor=processor)
    # Use the
    create_backtest.pipe([
        Pipeline(name="VerifyBacktest",
                 processor=processor,
                 steps=[
                     CheckUniverse(),
                     CheckStrategy(),
                     CreateBacktestComponent()
                 ])
    ])

    episode_attachment = AttachToEpisode()
    episode_attachment.processor = processor
    # Use this pipeline to setup a backtest to be run
    setup_backtest = (Pipeline(name="SetupBacktest",
                               processor=processor,
                               steps=[
                                   CreateEpisodePortfolio(),
                                   CreateRequirements(),
                                   episode_attachment
                               ]))

    backtest_config = create_backtest_config()
    created_backtest = create_backtest.step(backtest_config,
                                            # override=True,
                                            is_loud=False)
    ran_backtest = setup_backtest.step(created_backtest, is_loud=False)
    strategyid = episode_attachment.spec.strategy_by_episode(ran_backtest.current_episode)
    strat_engine = StrategyEngine(processor=processor)
    current_strategy_engine = strat_engine.pick(strategyid)
    current_strategy = current_strategy_engine.strategy
    logger.critical(current_strategy)


if __name__ == "__main__":
    main()
