#!/usr/bin/env python3
# Copyright 2020-present NAVER Corp. See LICENSE file for license details

"""
All base kapture objects, with their reading and writing functions on disk,
and the conversion from and to other formats.
"""

from .core import *
# silence kapture logging to critical only, except if told otherwise
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.CRITICAL)
