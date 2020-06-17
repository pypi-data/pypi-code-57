"""The simple detector implementation"""
# pylint: disable=E1101,R0801
from dataclasses import dataclass, field
from datetime import datetime
from typing import Tuple
from uuid import uuid4

import numpy as np  # type: ignore
import cv2 as cv  # type: ignore

from detection.detector import Detector, DetectionType, MetadataType


@dataclass
class SimpleDetector(Detector):
    """The simplest frame difference-based motion detector"""

    _width: int = field(default=1)
    _height: int = field(default=1)
    _previous_frame: cv.UMat = field(default=cv.UMat(np.zeros([1, 1, 1], dtype=np.uint8)), repr=False)
    _latest_frame: cv.UMat = field(default=cv.UMat(np.zeros([1, 1, 1], dtype=np.uint8)), repr=False)

    @staticmethod
    def preprocess(frame: np.array) -> cv.UMat:
        """Ensure a frame is a grayscale UMat"""
        if frame.shape[2] == 1:
            return cv.UMat(frame)
        if frame.shape[2] == 3:
            return cv.cvtColor(cv.UMat(frame), cv.COLOR_BGR2GRAY)
        raise ValueError("Can only consume 1- and 3-channel images.")

    def feed(self, frame: np.array) -> Tuple[DetectionType, MetadataType]:
        """Feed a frame in"""

        _frame = SimpleDetector.preprocess(frame)

        # If incoming frame's dimensions differ from latest seen, reset everything and return
        if frame.shape[1] != self._width or frame.shape[0] != self._height:
            self._width, self._height = frame.shape[1], frame.shape[0]
            self._latest_frame = _frame
            self._previous_frame = cv.UMat(self._latest_frame)
            self._detections = {}
            return (self._detections, self._metadata)

        # Shift frames
        self._previous_frame = cv.UMat(self._latest_frame)
        self._latest_frame = _frame

        # Calculate frame difference
        mean = cv.mean(cv.absdiff(self._latest_frame, self._previous_frame))[0]

        # Decide if there's a detection
        if mean >= self.config["threshold"] * 256:
            self._detections = {(uuid4(), datetime.utcnow()): (0, 0, self._width - 1, self._height - 1)}
        else:
            self._detections = {}

        return (self._detections, self._metadata)
