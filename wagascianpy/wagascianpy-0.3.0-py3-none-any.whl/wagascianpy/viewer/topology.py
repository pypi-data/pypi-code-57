#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio
#

from collections import namedtuple
from typing import List

import pygubu

DetectorState = namedtuple('State', ['index', 'enabled'])


class Topology(object):
    """List of enabled and disabled detectors"""

    def __init__(self):
        self.WallmrdNorthTop = DetectorState(0, True)
        self.WallmrdNorthBottom = DetectorState(1, True)
        self.WallmrdSouthTop = DetectorState(2, True)
        self.WallmrdSouthBottom = DetectorState(3, True)
        self.WagasciUpstreamTop = DetectorState(4, True)
        self.WagasciUpstreamSide = DetectorState(5, True)
        self.WagasciDownstreamTop = DetectorState(6, True)
        self.WagasciDownstreamSide = DetectorState(7, True)

    def are_all_enabled(self):
        # type: (...) -> bool
        for value in vars(self).values():
            if value.enabled is False:
                return False
        return True

    def get_all(self):
        # type: (...) -> List[DetectorState]
        return [value for value in vars(self).values()]

    def get_enabled(self):
        # type: (...) -> List[DetectorState]
        return [value for value in vars(self).values() if value.enabled is True]

    def get_disabled(self):
        # type: (...) -> List[DetectorState]
        return [value for value in vars(self).values() if value.enabled is False]

    # noinspection PyProtectedMember
    def read_topology(self, builder):
        # type: (pygubu.Builder) -> None
        self.WallmrdNorthTop = self.WallmrdNorthTop._replace(
            enabled=builder.tkvariables.__getitem__('wallmrd_top_north').get())
        self.WallmrdNorthBottom = self.WallmrdNorthBottom._replace(
            enabled=builder.tkvariables.__getitem__('wallmrd_bottom_north').get())
        self.WallmrdSouthTop = self.WallmrdSouthTop._replace(
            enabled=builder.tkvariables.__getitem__('wallmrd_top_south').get())
        self.WallmrdSouthBottom = self.WallmrdSouthBottom._replace(
            enabled=builder.tkvariables.__getitem__('wallmrd_bottom_south').get())
        self.WagasciUpstreamTop = self.WagasciUpstreamTop._replace(
            enabled=builder.tkvariables.__getitem__('wagasci_top_upstream').get())
        self.WagasciUpstreamSide = self.WagasciUpstreamSide._replace(
            enabled=builder.tkvariables.__getitem__('wagasci_side_upstream').get())
        self.WagasciDownstreamTop = self.WagasciDownstreamTop._replace(
            enabled=builder.tkvariables.__getitem__('wagasci_top_downstream').get())
        self.WagasciDownstreamSide = self.WagasciDownstreamSide._replace(
            enabled=builder.tkvariables.__getitem__('wagasci_side_downstream').get())
