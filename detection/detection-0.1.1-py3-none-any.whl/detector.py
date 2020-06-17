"""The detector base class"""
# pylint: disable=E1101,R0801

from abc import ABC
from dataclasses import dataclass, field
from typing import Any, Tuple, Dict
from datetime import datetime
from uuid import UUID

import numpy as np  # type: ignore

ConfigType = Dict[str, Any]
DetectionType = Dict[Tuple[UUID, datetime], Tuple[int, int, int, int]]
MetadataType = Dict[str, Any]


@dataclass
class Detector(ABC):
    """The detector base class"""

    config: Dict[str, Any] = field(default_factory=dict)
    _detections: DetectionType = field(default_factory=dict)
    _metadata: MetadataType = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Default to enabling GPU acceleration"""
        if not "accelerate" in self.config:
            self.config["accelerate"] = True
        if not "learningrate" in self.config:
            self.config["learningrate"] = 0.001

    def feed(self, frame: np.array) -> Tuple[DetectionType, MetadataType]:  # Didn't use numpy-stubs
        """Feed a frame in"""
        raise NotImplementedError()
