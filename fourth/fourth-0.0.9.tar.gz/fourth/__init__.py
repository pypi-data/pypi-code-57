"""
The Fourth datetime library. ALl public names should be imported here and
declared in __all__.

TODO feature list:
* spanning datetime type
* Full type annotations
* Full docstrings
* future imports
* full test suite
* set up coverage on CI
* setup changelog - semantic version statement
* Docs
"""
from __future__ import annotations

__version__ = "0.0.9"

__all__ = ("LocalDatetime", "UTCDatetime")

from .types import LocalDatetime, UTCDatetime
