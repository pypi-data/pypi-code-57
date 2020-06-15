# -*- coding: utf-8 -*-
"""
module for base class
"""

from abc import (
    ABC,
    abstractmethod,
)
from pathlib import Path

import cv2

from sail_utils import LOGGER


class _Streamer(ABC):

    def __init__(self, source: str, rate: float):
        self._source = Path(source)
        self._rate = rate
        self._stream = None

    @property
    def source(self) -> str:
        """
        get the source
        :return:
        """
        return self._source.as_posix()

    @property
    def rate(self) -> float:
        """
        get the sampling rate
        :return:
        """
        return self._rate

    @property
    def stream(self):
        """
        get the internal stream
        :return:
        """
        return self._stream


class _Detector(ABC):

    def __init__(self,
                 server: str,
                 src_size: int,
                 dst_size: int,
                 threshold: float,
                 timeout: float):
        self._server = server
        self._threshold = threshold
        self._mapper = _Mapper(src_size, dst_size)
        self._timeout = timeout
        LOGGER.info(f"detector at: <{self._server}> with threshold <{self._threshold:.2f}>")

    @abstractmethod
    def detect(self, img, epoch) -> list:
        """
        method to detect a image
        :param img:
        :param epoch:
        :return:
        """

    def __str__(self):
        return f"mapper: {self._mapper}\nserver: {self._server}"


class _Mapper:

    def __init__(self, src: int, dst: int):
        self._src = src
        self._dst = dst
        LOGGER.info(f"mapper from <{self._src}> to <{self._dst}>")

    def resize(self, img):
        """
        resize pic to destination size
        :param img:
        :return:
        """
        return cv2.resize(img, (self._dst, self._dst), interpolation=cv2.INTER_AREA)

    def __call__(self, bbox):
        scale = self._src / self._dst
        return [
            int(bbox[0] * scale),
            int(bbox[1] * scale),
            int(bbox[2] * scale),
            int(bbox[3] * scale),
        ]

    def __str__(self):
        return f"source: <{self._src} - destination: <{self._dst}>"
