# -*- coding: utf-8 -*-
import logging as log
import sys

from . import general, gui
from .servo import Servo
from .servodevice import ServoDevice

if sys.version_info >= (3, 8):
    import importlib.metadata as metadata  # Python 3.8 pylint: disable=import-error
else:
    import importlib_metadata as metadata  # <= Python 3.7 pylint: disable=import-error

try:
    __version__ = metadata.version(__name__)
except metadata.PackageNotFoundError:
    __version__ = "unknown"
    log.warning("Version not known, importlib.metadata is not working correctly.")
