"""MOG2 detector implementation"""
# pylint: disable=E1101,R0801
from dataclasses import dataclass, field
from datetime import datetime
from time import time
from typing import Any, Tuple
from uuid import uuid4

import numpy as np  # type: ignore
import cv2 as cv  # type: ignore

from detection.detector import Detector, DetectionType, MetadataType


@dataclass
class BlobDetector(Detector):
    """MOG2 motion detector"""

    _width: int = field(default=1)
    _height: int = field(default=1)
    _subtractor: Any = field(default=cv.createBackgroundSubtractorMOG2(), repr=False)
    _stabilize: int = field(default=100)

    def __post_init__(self) -> None:
        """Disable or enable OpenCL"""
        if "accelerate" in self.config and self.config["accelerate"]:
            cv.ocl.setUseOpenCL(True)
        else:
            cv.ocl.setUseOpenCL(False)

    def preprocess(self, frame: np.array) -> cv.UMat:
        """Ensure a frame is an UMat"""
        if not frame.shape[2] in (1, 3):
            raise ValueError("Can only consume 1- and 3-channel images.")
        if "accelerate" in self.config and self.config["accelerate"]:
            _time = time()
            _frame = cv.UMat(frame)
            self._metadata["took"].append(("cv.UMat", time() - _time))
        else:
            _frame = frame
        if "blur" in self.config:
            blur = self.config["blur"]
            if blur < 3 or not blur % 2:
                raise ValueError("Blur kernel size should be and odd value >= 3.")
            _time = time()
            _frame = cv.GaussianBlur(_frame, (blur, blur), 0)
            self._metadata["took"].append(("cv.GaussianBlur", time() - _time))
        return cv.UMat(frame)

    def feed(self, frame: np.array) -> Tuple[DetectionType, MetadataType]:
        """Feed a frame in"""

        self._detections = {}
        self._metadata = {"start_timestamp": datetime.utcnow(), "took": []}
        _frame = self.preprocess(frame)

        # If incoming frame's dimensions differ from latest seen, reset everything and return
        if frame.shape[1] != self._width or frame.shape[0] != self._height:
            self._width, self._height = frame.shape[1], frame.shape[0]
            self._subtractor = cv.createBackgroundSubtractorMOG2()
            self._subtractor.apply(_frame)
            return (self._detections, {})

        # Feed frame to subtractor
        _time = time()
        mask = self._subtractor.apply(_frame, learningRate=0.001)
        self._metadata["took"].append(("cv.BackgroundSubtractorMOG2.apply", time() - _time))

        # Find contours
        _time = time()
        contours, _ = cv.findContours(mask, mode=cv.RETR_EXTERNAL, method=cv.CHAIN_APPROX_SIMPLE)
        self._metadata["took"].append(("cv.findContours", time() - _time))

        # Find blobs
        for contour in contours:
            _time = time()
            polygon = cv.approxPolyDP(contour, epsilon=3, closed=True)
            self._metadata["took"].append(("cv.approxPolyDP", time() - _time))

            _time = time()
            boundingbox = cv.boundingRect(polygon)
            self._metadata["took"].append(("cv.boundingRect", time() - _time))

            self._detections[(uuid4(), self._metadata["start_timestamp"])] = (
                boundingbox[0],
                boundingbox[1],
                boundingbox[0] + boundingbox[2],
                boundingbox[1] + boundingbox[3],
            )

        self._metadata["end_timestamp"] = datetime.utcnow()
        self._metadata["took"].append(
            ("total", (self._metadata["end_timestamp"] - self._metadata["start_timestamp"]).total_seconds())
        )

        return (self._detections, self._metadata)
