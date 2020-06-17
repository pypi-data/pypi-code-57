"""The detector factory"""

from typing import Any

from detection.detector import ConfigType
from detection.helpers import import_detector


def make_detector(friendlyname: str = "simple", config: ConfigType = dict()) -> Any:  # pylint: disable=W0102
    """Make a detector"""
    return import_detector(friendlyname)(config)
