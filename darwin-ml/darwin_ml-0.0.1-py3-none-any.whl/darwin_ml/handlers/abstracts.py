import pprint
import time
import uuid
import warnings
from abc import ABC, abstractmethod, abstractproperty
from typing import Any, Dict, List, Optional, Union

import maya
from jamboree import BaseHandler, Jamboree, TimeHandler
from jamboree.handlers.default import DataHandler
from jamboree.utils.support.search import querying
from loguru import logger
from pydantic import BaseModel

from darwin_ml.technical import fiboacci_general, fibonacci
from darwin_ml.utils import Injectable

warnings.simplefilter(action='ignore', category=FutureWarning)


class StateTransformerAbstract(Injectable, ABC):
    """StateTransformer

    Arguments:
        ABC {Abstract} -- An abstract to be inheritted by future classes
    """
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.__state: Optional[Any] = None
        self.__handler: Optional[BaseHandler] = None
        # State Model
        self.__smodel: Optional[BaseModel] = None
        # Parameter Model
        self.__pmodel: Optional[BaseModel] = None
        # Step Model
        self.__stmodel: Optional[BaseModel] = None
        self.__time = TimeHandler()
        self.__episode: str = "live"
        self.__live: bool = False

    @property
    def time(self) -> TimeHandler:
        """The time handler used to get the current time.

        Returns:
            TimeHandler -- The time handler with the state loaded into it.
        """
        self.__time.processor = self.processor
        self.__time['episode'] = self.episode
        self.__time['live'] = self.live
        self.__time.reset()
        return self.__time

    @property
    def current_time(self) -> float:
        return self.time.head

    @property
    def episode(self) -> str:
        return self.__episode

    @episode.setter
    def episode(self, _episode: str):
        self.__episode = _episode

    @property
    def live(self) -> bool:
        return self.__live

    @live.setter
    def live(self, _live: bool):
        self.__live = _live

    @abstractproperty
    def state_model(self):
        raise NotImplementedError("State model not implemented.")

    @abstractproperty
    def param_model(self):
        raise NotImplementedError("Parameter model not implemented.")

    @abstractproperty
    def step_model(self):
        raise NotImplementedError("Step model not implemented.")

    @abstractproperty
    def state(self) -> Union[type]:
        raise NotImplementedError("State property not set")

    @abstractmethod
    def set_params(self, **kwargs):
        raise NotImplementedError("Parameters not set")

    @abstractmethod
    def reset(self):
        raise NotImplementedError("Reset function not implemented")

    @abstractmethod
    def step(self) -> BaseModel:
        """Take a single step necessary to create a state space.

        Raises:
            NotImplementedError: If the abstract method wasn't overwritten

        Returns:
            BaseModel -- A type constrained model to return all of the variables
        """
        raise NotImplementedError("Step function not implemented")
    
    def display_state(self):
        ts = maya.MayaDT(self.current_time)
        ep = self.episode
        lv = self.live
        state_message = f"\n\n The current time: {ts}\n\n Current Episode: {ep}\n\n Is Live: {lv}"
        logger.debug(state_message)


class TAPriceData(DataHandler):
    """
        # TAPriceData

        A way to store ta_features for the.
    """
    def __init__(self):
        super().__init__()
        self['category'] = "markets"
        self['submetatype'] = "technical"

