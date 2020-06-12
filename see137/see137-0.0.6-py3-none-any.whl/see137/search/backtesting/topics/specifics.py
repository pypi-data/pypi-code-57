import uuid
import maya

from typing import Optional, List
from jamboree import Jamboree
from jamboree.base.processors.abstracts import Processor
from jamboree.handlers.abstracted.search import ParameterizedSearch
from jamboree.handlers.default.search import BaseSearchHandler
from see137.search.prototype import SearchFacade
from loguru import logger


class EpisodeSpecificInformationSearch(BaseSearchHandler):
    """
        A search handler for all episode specific information. Use to find related information per episode.

        This is a variation of session specific information, which we'll use to get reward function by episode.

        
    """
    def __init__(self):
        super().__init__()

        self.entity = "episodespec"
        self.dreq = {
            'episode': str,
            'backtest': str,
            'strategy': str,
            'portfolio': str
        }


class BacktestEpisodeSpec(SearchFacade):
    def __init__(self):
        ProcedureSearch = EpisodeSpecificInformationSearch()
        super().__init__(ProcedureSearch)
        self.must_have = ['episode']

    def strategy_by_episode(self, episode: str):
        strategies = self.Find(episode=episode)
        if len(strategies) > 0:
            strategy_dict = strategies[0]
            strategy_id = strategy_dict['strategy']
            return strategy_id
        raise AttributeError("Strategy Doesn't Exist")