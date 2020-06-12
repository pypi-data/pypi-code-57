#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from .glcollection import GLCollection

from ..drawables.backgroundgl import BackgroundGL
from ..glprograms.backgroundprogram import BackgroundProgram


class GLBackgroundCollection(GLCollection):
    def __init__(self, viewer=None):
        super().__init__(viewer)
        self.associate(BackgroundProgram(viewer), lambda: self.retrieve(BackgroundGL))
