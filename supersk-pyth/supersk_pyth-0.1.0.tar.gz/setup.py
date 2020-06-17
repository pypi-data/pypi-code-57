#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from setuptools import setup


if sys.version_info.major < 3:
    raise RuntimeError(
            "Pyth does not support Python 2.x."
            "Please use Python 3.")

setup()
