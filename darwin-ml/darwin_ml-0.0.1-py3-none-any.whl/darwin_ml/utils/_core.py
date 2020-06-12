import uuid
from abc import ABC
from typing import Optional
from jamboree import Jamboree
from jamboree.handlers import TimeHandler

class Injectable(ABC):
    def __init__(self):
        self.__processor: Optional[Jamboree] = None
        self.__asset: Optional[str] = None
        self.__episode: str = uuid.uuid4().hex
        self.__live: bool = False

    @property
    def processor(self) -> Jamboree:
        if self.__processor is None:
            raise ValueError("The processor needs to be set")
        return self.__processor

    @processor.setter
    def processor(self, __processor: Jamboree):
        self.__processor = __processor


class InjectableTime(Injectable):
    def __init__(self):
        # super().__init__()
        self.__asset: Optional[str] = None
        self.__episode: str = uuid.uuid4().hex
        self.__live: bool = False
        self.__time: TimeHandler = TimeHandler()

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
    
    @property
    def asset(self) -> str:
        if self.__asset is None:
            raise ValueError("The asset hasn't been set yet.")
        return self.__asset

    @asset.setter
    def asset(self, _asset: str):
        self.__asset = _asset