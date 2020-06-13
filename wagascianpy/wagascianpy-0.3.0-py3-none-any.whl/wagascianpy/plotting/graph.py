#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

from collections import namedtuple

import numpy
from six import string_types

import wagascianpy.plotting.colors

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

Range = namedtuple('Range', ['lower_bound', 'upper_bound'])


class Graph(object):

    def __init__(self, title, graph_id=None):
        self.title = title
        self.id = graph_id if graph_id is not None else title
        self._xdata = None
        self._ydata = None
        self._color = wagascianpy.plotting.colors.Colors.Black.value
        self._xrange = Range(lower_bound=None, upper_bound=None)
        self._yrange = Range(lower_bound=None, upper_bound=None)
        self._is_empty = True

    @property
    def xdata(self):
        return self._xdata

    @xdata.setter
    def xdata(self, xdata):
        if isinstance(xdata, list):
            self._xdata = numpy.asarray(xdata, dtype=numpy.float64)
        elif isinstance(xdata, numpy.ndarray):
            self._xdata = xdata
        elif xdata is None:
            self._xdata = numpy.array([], dtype=numpy.float64)
        else:
            raise TypeError("Data format not recognized : type(ydata) = {}".format(type(xdata).__name__))
        assert self._xdata.dtype == numpy.float64
        if self._xdata.size == 0:
            self._is_empty = True
        else:
            self._is_empty = False

    @property
    def ydata(self):
        return self._ydata

    @ydata.setter
    def ydata(self, ydata):
        if isinstance(ydata, list):
            self._ydata = numpy.asarray(ydata, dtype=numpy.float64)
        elif isinstance(ydata, numpy.ndarray):
            self._ydata = ydata
        elif ydata is None:
            self._ydata = numpy.array([], dtype=numpy.float64)
        else:
            raise TypeError("Data format not recognized : type(ydata) = {}".format(type(ydata).__name__))
        assert self._ydata.dtype == numpy.float64
        if self._ydata.size == 0:
            self._is_empty = True
        else:
            self._is_empty = False

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        if isinstance(color, int):
            self._color = color
        elif isinstance(color, wagascianpy.plotting.colors.Colors):
            self._color = color.value
        elif isinstance(color, string_types):
            self._color = wagascianpy.plotting.colors.Colors.get_by_detector(color).value
        else:
            raise TypeError("Color type is unknown {}".format(type(color).__name__))

    @property
    def xrange(self):
        return self._xrange

    @xrange.setter
    def xrange(self, xrange):
        if isinstance(xrange, Range):
            self._xrange = xrange
        else:
            raise TypeError("X axis Range type is unknown {}".format(type(xrange).__name__))

    @property
    def yrange(self):
        return self._yrange

    @yrange.setter
    def yrange(self, yrange):
        if isinstance(yrange, Range):
            self._yrange = yrange
        else:
            raise TypeError("Y axis Range type is unknown {}".format(type(yrange).__name__))

    def is_empty(self):
        return self._is_empty

    def make_tgraph(self):
        if self._xdata is None or self._ydata is None:
            raise RuntimeError("Please insert some data in the graph")
        if len(self._xdata) != len(self._ydata):
            raise IndexError("xdata ({}) and ydata ({}) length mismatch".format(len(self._xdata), len(self._ydata)))
        tgraph = ROOT.TGraph(len(self._xdata), self._xdata, self._ydata)
        tgraph.SetNameTitle(self.id, self.title)
        tgraph.SetLineColor(self._color)
        tgraph.SetMarkerColor(self._color)
        x_lower_bound = self._xrange.lower_bound if self._xrange.lower_bound is not None else \
            numpy.amin(self._xdata)
        x_upper_bound = self._xrange.upper_bound if self._xrange.upper_bound is not None else \
            numpy.amax(self._xdata)
        y_lower_bound = self._yrange.lower_bound if self._yrange.lower_bound is not None else \
            numpy.amin(self._ydata)
        y_upper_bound = self._yrange.upper_bound if self._yrange.upper_bound is not None else \
            numpy.amax(self._ydata)
        tgraph.GetXaxis().SetLimits(x_lower_bound, x_upper_bound)
        tgraph.GetHistogram().SetMaximum(y_upper_bound)
        tgraph.GetHistogram().SetMinimum(y_lower_bound)
        return tgraph
