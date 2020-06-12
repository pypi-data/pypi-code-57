import uuid
import maya

from typing import Optional
from jamboree import Jamboree
from jamboree.base.processors.abstracts import Processor
from see137.search.backtesting.topics import backtests as bts
from see137.search.backtesting.topics import episodes as eps
from see137.search.backtesting.topics import strategy as sst
from see137.search.backtesting.topics import universe as uni
from see137.search.backtesting.topics.asset import universal as unias

class CreateAccessor:
    def __init__(self):
        self._processor: Optional[Processor] = None
        self._backtest = bts.BacktestCreate()
        self._episodes = eps.EpisodeCreate()
        self._strategy = sst.StrategyCreate()
        self._universe = uni.UniverseCreate()
        self._unias = unias.UniverseAssetCreate()
        # self._universe_detail = univo.UniverseDetailCreate()

    @property
    def processor(self):
        if self._processor is None:
            raise AttributeError("Processor hasn't been set for create calls in search.")
        return self._processor

    @processor.setter
    def processor(self, _processor):
        self._processor = _processor

    @property
    def backtest(self):
        self._backtest.processor = self.processor
        return self._backtest
    
    @property
    def episodes(self):
        self._episodes.processor = self.processor
        return self._episodes
    
    @property
    def strategy(self):
        self._strategy.processor = self.processor
        return self._strategy

    @property
    def universe(self):
        self._universe.processor = self.processor
        return self._universe
    
    @property
    def universe_asset(self):
        self._unias.processor = self.processor
        return self._unias


class InfoAccessor:
    def __init__(self):
        self._processor: Optional[Processor] = None
        self._backtest = bts.BacktestInfo()
        self._episodes = eps.EpisodeInfo()
        self._strategy = sst.StrategyInfo()
        self._universe = uni.UniverseInfo()
        self._unias = unias.UniverseAssetInfo()

    @property
    def processor(self):
        if self._processor is None:
            raise AttributeError("Processor hasn't been set for create calls in search.")
        return self._processor

    @processor.setter
    def processor(self, _processor):
        self._processor = _processor

    @property
    def backtest(self):
        self._backtest.processor = self.processor
        return self._backtest
    
    @property
    def episodes(self):
        self._episodes.processor = self.processor
        return self._episodes
    
    @property
    def strategy(self):
        self._strategy.processor = self.processor
        return self._strategy

    @property
    def universe(self):
        self._universe.processor = self.processor
        return self._universe
    
    @property
    def universe_asset(self):
        self._unias.processor = self.processor
        return self._unias


class RemoveAccessor:
    def __init__(self):
        self._processor: Optional[Processor] = None
        self._backtest = bts.BacktestRemove()
        self._episodes = eps.EpisodeRemove()
        self._strategy = sst.StrategyRemove()
        self._universe = uni.UniverseRemove()
        self._unias = unias.UniverseAssetsRemove()


    @property
    def processor(self):
        if self._processor is None:
            raise AttributeError("Processor hasn't been set for create calls in search.")
        return self._processor

    @processor.setter
    def processor(self, _processor):
        self._processor = _processor


    @property
    def backtest(self):
        self._backtest.processor = self.processor
        return self._backtest
    
    @property
    def episodes(self):
        self._episodes.processor = self.processor
        return self._episodes
    
    @property
    def strategy(self):
        self._strategy.processor = self.processor
        return self._strategy

    @property
    def universe(self):
        self._universe.processor = self.processor
        return self._universe
    
    @property
    def universe_asset(self):
        self._unias.processor = self.processor
        return self._unias


class UpdateAccessor:
    def __init__(self):
        self._processor: Optional[Processor] = None
        self._backtest = bts.BacktestUpdate()
        self._episodes = eps.EpisodeUpdate()
        self._strategy = sst.StrategyUpdate()
        self._universe = uni.UniverseUpdate()
        self._unias = unias.UniverseAssetUpdate()

    @property
    def processor(self):
        if self._processor is None:
            raise AttributeError("Processor hasn't been set for create calls in search.")
        return self._processor

    @processor.setter
    def processor(self, _processor):
        self._processor = _processor
    

    @property
    def backtest(self):
        self._backtest.processor = self.processor
        return self._backtest
    
    @property
    def episodes(self):
        self._episodes.processor = self.processor
        return self._episodes
    
    @property
    def strategy(self):
        self._strategy.processor = self.processor
        return self._strategy

    @property
    def universe(self):
        self._universe.processor = self.processor
        return self._universe
    
    @property
    def universe_asset(self):
        self._unias.processor = self.processor
        return self._unias