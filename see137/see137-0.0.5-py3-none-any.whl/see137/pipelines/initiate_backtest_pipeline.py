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
from see137.components.strategy import CheckStrategy
from see137.components.universe import CheckUniverse
from see137.handlers.strategy.core import StrategyEngine
from see137.models.backtests_models import BacktestConfig
from see137.search.prototype import SearchFacade
from see137.components.portfolio import CreateEpisodePortfolio
from see137.components.requirements import AttachToEpisode, CreateRequirements



class BacktestInitiationPipeline(Pipeline):
    def __init__(self, processor:Jamboree):
        super().__init__(name="SetupBacktest", processor=processor)
        self.pipe([CheckStrategy(), CheckUniverse()])
        self.pipe(CreateEpisodePortfolio())
        self.pipe(CreateRequirements())
        self.pipe(AttachToEpisode())