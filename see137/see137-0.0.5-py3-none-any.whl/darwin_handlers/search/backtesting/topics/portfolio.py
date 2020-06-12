import uuid
import maya

from typing import Optional, List
from jamboree import Jamboree
from jamboree.base.processors.abstracts import Processor
from jamboree.handlers.abstracted.search import ParameterizedSearch
from jamboree.handlers.default.search import BaseSearchHandler
from see137.search.prototype import SearchFacade
from loguru import logger

class AggregatePortfolio(BaseSearchHandler):
    """A search handler the aggregate portfolio

    Arguments:
        BaseSearchHandler {[type]} -- [description]
    """
    def __init__(self):
        super().__init__()

        self.entity = "aggregate_portfolio"
        self.dreq = {
            'timestamp': float,
            'episode': str,
            "user": str,
            'total': float,
            "allocation": dict,
            'performance': float
        }

class BacktestPortfolioAgg(SearchFacade):
    def __init__(self):
        ProcedureSearch = AggregatePortfolio()
        super().__init__(ProcedureSearch)
        self.must_have = ['episode']