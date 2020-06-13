#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

from recordclass import recordclass


class Topology(object):
    """List of enabled and disabled detectors"""

    def __init__(self, iterate_by_dif=False):
        state = recordclass('state', ['name', 'enabled', 'by_dif'])
        self.iterate_by_dif = iterate_by_dif
        self._wallmrd_north = state("WallMRD north", True, False)
        self._wallmrd_south = state("WallMRD south", True, False)
        self._wagasci_upstream = state("WAGASCI upstream", True, False)
        self._wagasci_downstream = state("WAGASCI downstream", True, False)
        self._wallmrd_north_top = state("WallMRD north top", True, True)
        self._wallmrd_north_bottom = state("WallMRD north bottom", True, True)
        self._wallmrd_south_top = state("WallMRD south top", True, True)
        self._wallmrd_south_bottom = state("WallMRD south bottom", True, True)
        self._wagasci_upstream_top = state("WAGASCI upstream top", True, True)
        self._wagasci_upstream_side = state("WAGASCI upstream side", True, True)
        self._wagasci_downstream_top = state("WAGASCI downstream top", True, True)
        self._wagasci_downstream_side = state("WAGASCI downstream side", True, True)

    @property
    def wallmrd_north(self):
        return self._wallmrd_north

    @wallmrd_north.setter
    def wallmrd_north(self, wallmrd_north):
        self._wallmrd_north = wallmrd_north
        self._wallmrd_north_top.enabled = self._wallmrd_north.enabled
        self._wallmrd_north_bottom.enabled = self._wallmrd_north.enabled

    @property
    def wallmrd_north_top(self):
        return self._wallmrd_north_top

    @wallmrd_north_top.setter
    def wallmrd_north_top(self, wallmrd_north_top):
        self._wallmrd_north_top = wallmrd_north_top
        self._wallmrd_north = self._wallmrd_north_top.enabled and self._wallmrd_north_bottom.enabled

    @property
    def wallmrd_north_bottom(self):
        return self._wallmrd_north_bottom

    @wallmrd_north_bottom.setter
    def wallmrd_north_bottom(self, wallmrd_north_bottom):
        self._wallmrd_north_top = wallmrd_north_bottom
        self._wallmrd_north = self._wallmrd_north_top.enabled and self._wallmrd_north_bottom.enabled

    @property
    def wallmrd_south(self):
        return self._wallmrd_south

    @wallmrd_south.setter
    def wallmrd_south(self, wallmrd_south):
        self._wallmrd_south = wallmrd_south
        self._wallmrd_south_top.enabled = self._wallmrd_south.enabled
        self._wallmrd_south_bottom.enabled = self._wallmrd_south.enabled

    @property
    def wallmrd_south_top(self):
        return self._wallmrd_south_top

    @wallmrd_south_top.setter
    def wallmrd_south_top(self, wallmrd_south_top):
        self._wallmrd_south_top = wallmrd_south_top
        self._wallmrd_south = self._wallmrd_south_top.enabled and self._wallmrd_south_bottom.enabled

    @property
    def wallmrd_south_bottom(self):
        return self._wallmrd_south_bottom

    @wallmrd_south_bottom.setter
    def wallmrd_south_bottom(self, wallmrd_south_bottom):
        self._wallmrd_south_top = wallmrd_south_bottom
        self._wallmrd_south = self._wallmrd_south_top.enabled and self._wallmrd_south_bottom.enabled

    @property
    def wagasci_upstream(self):
        return self._wagasci_upstream

    @wagasci_upstream.setter
    def wagasci_upstream(self, wagasci_upstream):
        self._wagasci_upstream = wagasci_upstream
        self._wagasci_upstream_top.enabled = self._wagasci_upstream.enabled
        self._wagasci_upstream_side.enabled = self._wagasci_upstream.enabled

    @property
    def wagasci_upstream_top(self):
        return self._wagasci_upstream_top

    @wagasci_upstream_top.setter
    def wagasci_upstream_top(self, wagasci_upstream_top):
        self._wagasci_upstream_top = wagasci_upstream_top
        self._wagasci_upstream = self._wagasci_upstream_top.enabled and self._wagasci_upstream_side.enabled

    @property
    def wagasci_upstream_side(self):
        return self._wagasci_upstream_side

    @wagasci_upstream_side.setter
    def wagasci_upstream_side(self, wagasci_upstream_side):
        self._wagasci_upstream_top = wagasci_upstream_side
        self._wagasci_upstream = self._wagasci_upstream_top.enabled and self._wagasci_upstream_side.enabled

    @property
    def wagasci_downstream(self):
        return self._wagasci_downstream

    @wagasci_downstream.setter
    def wagasci_downstream(self, wagasci_downstream):
        self._wagasci_downstream = wagasci_downstream
        self._wagasci_downstream_top.enabled = self._wagasci_downstream.enabled
        self._wagasci_downstream_side.enabled = self._wagasci_downstream.enabled

    @property
    def wagasci_downstream_top(self):
        return self._wagasci_downstream_top

    @wagasci_downstream_top.setter
    def wagasci_downstream_top(self, wagasci_downstream_top):
        self._wagasci_downstream_top = wagasci_downstream_top
        self._wagasci_downstream = self._wagasci_downstream_top.enabled and self._wagasci_downstream_side.enabled

    @property
    def wagasci_downstream_side(self):
        return self._wagasci_downstream_side

    @wagasci_downstream_side.setter
    def wagasci_downstream_side(self, wagasci_downstream_side):
        self._wagasci_downstream_top = wagasci_downstream_side
        self._wagasci_downstream = self._wagasci_downstream_top.enabled and self._wagasci_downstream_side.enabled

    def are_all_enabled(self):
        for value in self.__dict__.values():
            if value.enabled is False:
                return False
        return True

    def disable_all_but(self, one):
        for d in self:
            if d.name != one:
                d.enabled = False

    def get_all(self):
        if not self.iterate_by_dif:
            return [value for key, value in self.__dict__.items()
                    if key != "iterate_by_dif" and value.by_dif is False]
        else:
            return [value for key, value in self.__dict__.items()
                    if key != "iterate_by_dif" and value.by_dif is True]

    def get_enabled(self):
        if not self.iterate_by_dif:
            return [value for key, value in self.__dict__.items()
                    if key != "iterate_by_dif" and value.by_dif is False and value.enabled is True]
        else:
            return [value for key, value in self.__dict__.items()
                    if key != "iterate_by_dif" and value.by_dif is True and value.enabled is True]

    def get_disabled(self):
        if not self.iterate_by_dif:
            return [value for key, value in self.__dict__.items()
                    if key != "iterate_by_dif" and value.by_dif is False and value.enabled is False]
        else:
            return [value for key, value in self.__dict__.items()
                    if key != "iterate_by_dif" and value.by_dif is True and value.enabled is False]

    def __iter__(self):
        """ Returns the Iterator object """
        return TopologyIterator(self)


class TopologyIterator(object):
    def __init__(self, topology):
        # Difs object reference
        self._topology = topology
        # member variable to keep track of current index
        self._index = 0

    def __next__(self):
        """ Returns the next value from difs object's lists """
        if not self._topology.iterate_by_dif:
            if self._index == 0:
                result = self._topology.wallmrd_north
            elif self._index == 1:
                result = self._topology.wallmrd_south
            elif self._index == 2:
                result = self._topology.wagasci_upstream
            elif self._index == 3:
                result = self._topology.wagasci_downstream
            else:
                raise StopIteration
        else:
            if self._index == 0:
                result = self._topology.wallmrd_north_top
            elif self._index == 1:
                result = self._topology.wallmrd_north_bottom
            elif self._index == 2:
                result = self._topology.wallmrd_south_top
            elif self._index == 3:
                result = self._topology.wallmrd_south_bottom
            elif self._index == 4:
                result = self._topology.wagasci_upstream_top
            elif self._index == 5:
                result = self._topology.wagasci_upstream_side
            elif self._index == 6:
                result = self._topology.wagasci_downstream_top
            elif self._index == 7:
                result = self._topology.wagasci_downstream_side
            else:
                raise StopIteration
        self._index += 1
        return result
