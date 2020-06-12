"""
    # State Space Modelling and Testing

    The goal of this file is to test how iterating through the state space will work.

"""
import random
import time
import uuid
from pprint import pprint
from random import uniform
from typing import Optional

import maya
from creme import datasets, stream
from jamboree import Jamboree
from jamboree.handlers import TimeHandler
from loguru import logger
from see137.handlers.exchange import PortfolioHandler
from stochastic.continuous import FractionalBrownianMotion

from darwin_ml.handlers import TAPredictionTransformer, TAPriceData
from darwin_ml.middleware.containers import (AllocationContainer,
                                             FeaturesContainer, PriceContainer)
from darwin_ml.models import OnlineModels, PriceDeltaModel, StateSpaceModel
from darwin_ml.utils import Injectable, InjectableTime


def create_samples(n, mult=10, _add=100):
    fbm = FractionalBrownianMotion(hurst=0.7, t=1)
    s = fbm.sample(n)
    s = (s * mult) + _add
    return s


def create_allocation_samples(n):
    fbm = FractionalBrownianMotion(hurst=0.7, t=1)
    allocation = fbm.sample(n)
    pct_fill = [uniform(0, 1) for _ in range(n + 1)]

    return allocation, pct_fill


def single_feature():
    return {
        "feature_1": random.uniform(0, 1),
        "feature_2": random.uniform(0, 1),
        "feature_3": random.uniform(0, 1),
        "feature_4": random.uniform(0, 1),
    }


def create_fake_features(n):
    feature_set = [single_feature() for _ in range(n + 1)]
    return feature_set


def setup_time():
    new_time = maya.now().subtract(years=5)
    return new_time._epoch


class MainStateSpace(InjectableTime):
    def __init__(self):
        super().__init__()
        # Need to create a save and load script for this.
        self.__space: StateSpaceModel = StateSpaceModel()
        self.__technical: TAPredictionTransformer = TAPredictionTransformer()
        self.__time: TimeHandler = TimeHandler()
        self.__portfolio = PortfolioHandler()

        self.exchange: str = "binance"
        self.user_id: str = uuid.uuid4().hex
        self.is_mock: bool = False

    @property
    def is_next(self) -> bool:
        is_features = self.features.is_next
        is_price = self.price.is_next

        return is_features and is_price

    @property
    def space(self) -> StateSpaceModel:
        """ Should probably manage"""
        return self.__space

    @property
    def features(self) -> TAPriceData:
        return self.technical.features

    @property
    def price(self) -> TAPriceData:
        return self.technical.price

    @property
    def portfolio(self):
        self.__portfolio.processor = self.processor
        self.__portfolio.exchange = self.exchange
        self.__portfolio.user_id = self.user_id
        self.__portfolio.episode = self.episode
        self.__portfolio['live'] = self.live
        self.__portfolio.reset()
        return self.__portfolio

    @property
    def technical(self) -> TAPredictionTransformer:
        self.__technical.processor = self.processor
        self.__technical.asset = self.asset
        self.__technical.episode = self.episode
        self.__technical.live = self.live
        return self.__technical

    @property
    def current_time(self) -> float:
        return self.time.head

    @property
    def feature_count(self) -> int:
        return self.features.count()

    @property
    def price_count(self) -> int:
        return self.price.count()

    @property
    def price_container(self) -> PriceContainer:
        current_price_set = (
            self.price
                .closest_head_omitted()
        )
        current_price_set_back = (
            self.price
                .closest_peakback_by_omitted()
        )

        price_container = PriceContainer(
            current_price_set, 
            current_price_set_back
        )
        return price_container

    @property
    def feature_container(self) -> FeaturesContainer:
        current_feature_set = (
            self.features
                .closest_head_omitted()
        )
        current_feature_set_back = (
            self.features
                .closest_peakback_by_omitted()
        )
        feature_container = FeaturesContainer(
            current_feature_set,
            current_feature_set_back
        )
        return feature_container

    @property
    def allocation_container(self):
        meta = self.technical.meta_model
        abbv = meta.abbreviation
        allocation = self.portfolio.current_allocation(
            symbol=abbv, is_mocked=self.is_mock)
        fill_pct = self.portfolio.current_pct_worth(
            symbol=abbv, is_mocked=self.is_mock)
        allocation_container = AllocationContainer(allocation, fill_pct)
        return allocation_container

    @property
    def is_next_features(self) -> bool:
        return self.features.is_next

    def change_stepsize(self, microseconds: float = 1000, seconds: float = 0, minutes: float = 0, hours: float = 10, days: float = 0, weeks: float = 0) -> None:
        """Changes the step size for all variables.

        Args:
            microseconds (float, optional): milliseconds. Defaults to 1000.
            seconds (float, optional): seconds. Defaults to 0.
            minutes (float, optional): minutes. Defaults to 0.
            hours (float, optional): hours. Defaults to 10.
            days (float, optional): days. Defaults to 0.
            weeks (float, optional): weeks. Defaults to 0.
        """
        local_time = self.time
        local_time.change_stepsize(microseconds=microseconds, seconds=seconds,
                                   minutes=minutes, hours=hours, days=days, weeks=weeks)

    def change_lookback(self, microseconds: float = 1000, seconds: float = 0, minutes: float = 0, hours: float = 10, days: float = 0, weeks: float = 0) -> None:
        """Changes the lookback time for the simulation.

        Args:
            microseconds (float, optional): milliseconds. Defaults to 1000.
            seconds (float, optional): seconds. Defaults to 0.
            minutes (float, optional): minutes. Defaults to 0.
            hours (float, optional): hours. Defaults to 10.
            days (float, optional): days. Defaults to 0.
            weeks (float, optional): weeks. Defaults to 0.
        """
        local_time = self.time
        local_time.change_lookback(microseconds=microseconds, seconds=seconds,
                                   minutes=minutes, hours=hours, days=days, weeks=weeks)

    def step(self):
        feature_container = self.feature_container
        price_container = self.price_container
        allocation_container = self.allocation_container
        ss = self.space.step(allocation_container,
                             feature_container, price_container)
        return ss

    def reset(self):
        self.technical.reset()
