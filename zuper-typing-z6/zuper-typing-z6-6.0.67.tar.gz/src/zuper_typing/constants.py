import os
import sys
from typing import ClassVar

from . import logger

__all__ = ["PYTHON_36", "PYTHON_37", "ZuperTypingGlobals"]

PYTHON_36 = sys.version_info[1] == 6
PYTHON_37 = sys.version_info[1] == 7
NAME_ARG = "__name_arg__"  # XXX: repeated
ANNOTATIONS_ATT = "__annotations__"
DEPENDS_ATT = "__depends__"
INTERSECTION_ATT = "__intersection__"


class ZuperTypingGlobals:
    cache_enabled: ClassVar[bool] = False
    enable_type_checking: ClassVar[bool] = True
    enable_type_checking_difficult: ClassVar[bool] = True


class MakeTypeCache:
    cache = {}


circle_job = os.environ.get("CIRCLE_JOB", None)

if circle_job == "test-3.7-no-cache":  # pragma: no cover
    ZuperTypingGlobals.cache_enabled = False
    logger.warning("Disabling cache (zuper_typing:cache_enabled) due to circle_job.")


class DataclassHooks:
    dc_repr = None
    dc_str = None
