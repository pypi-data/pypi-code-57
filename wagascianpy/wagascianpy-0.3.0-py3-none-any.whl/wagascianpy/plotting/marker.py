#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

import abc
from collections import namedtuple

from six import string_types

import wagascianpy.database.wagascidb
import wagascianpy.plotting.colors

import ROOT

ROOT.PyConfig.IgnoreCommandLineOptions = True

# compatible with Python 2 *and* 3
try:
    # noinspection PyUnresolvedReferences
    IntTypes = (int, long)  # Python2
except NameError:
    IntTypes = int  # Python3
ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})

CustomEvent = namedtuple('CustomEvent', ['start', 'stop', 'duration', 'label'])
MarkerTuple = namedtuple('MarkerTuple', ['run', 'maintenance', 'trouble'])


class Marker(object):

    def __init__(self, left_position=None, left_text=None,
                 line_color=wagascianpy.plotting.colors.Colors.Black.value):
        self._line_color = None
        self._left_text = None
        self._left_position = None
        self.line_color = line_color
        self.left_text = left_text
        self.left_position = left_position

    @property
    def left_text(self):
        return self._left_text

    @left_text.setter
    def left_text(self, left_text):
        self._left_text = left_text

    @property
    def left_position(self):
        return self._left_position

    @left_position.setter
    def left_position(self, left_position):
        self._left_position = left_position

    @property
    def line_color(self):
        return self._line_color

    @line_color.setter
    def line_color(self, line_color):
        if isinstance(line_color, IntTypes):
            self._line_color = line_color
        elif isinstance(line_color, wagascianpy.plotting.colors.Colors):
            self._line_color = line_color.value
        elif isinstance(line_color, string_types):
            self._line_color = wagascianpy.plotting.line_colors.Colors.get_by_detector(line_color).value
        else:
            raise TypeError("line color type is unknown {}".format(type(line_color).__name__))

    def make_tobjects(self):
        left_markers = []
        ROOT.gPad.Modified()
        ROOT.gPad.Update()
        y_minimum = ROOT.gPad.GetUymin()
        y_maximum = ROOT.gPad.GetUymax()
        x_minimum = ROOT.gPad.GetUxmin()
        x_maximum = ROOT.gPad.GetUxmax()
        tline = ROOT.TLine(self.left_position, y_minimum, self.left_position, y_maximum)
        tline.SetLineColor(self.line_color)
        tline.SetLineWidth(1)
        tline.SetLineStyle(2)
        if self.left_text:
            ttext = ROOT.TText(self.left_position + (x_maximum - x_minimum) * 0.005,
                               0.98 * y_maximum, self.left_text)
            ttext.SetTextAngle(90)
            ttext.SetTextAlign(33)
            ttext.SetTextSize(0.03)
            ttext.SetTextColor(self.line_color)
            left_markers.append(ttext)
        left_markers.append(tline)
        return left_markers


class DoubleMarker(Marker):

    def __init__(self, left_position=None, left_text="",
                 line_color=wagascianpy.plotting.colors.Colors.Black.value,
                 right_position=None, right_text=""):
        super(DoubleMarker, self).__init__(left_position=left_position,
                                           left_text=left_text, line_color=line_color)
        self._right_text = None
        self._right_position = None
        self.right_text = right_text
        self.right_position = right_position
        self._transparency = None
        self._fill_color = None

    @property
    def right_text(self):
        return self._right_text

    @right_text.setter
    def right_text(self, right_text):
        self._right_text = right_text

    @property
    def right_position(self):
        return self._right_position

    @right_position.setter
    def right_position(self, right_position):
        self._right_position = right_position

    @property
    def fill_color(self):
        return self._fill_color

    @fill_color.setter
    def fill_color(self, fill_color):
        if isinstance(fill_color, int):
            self._fill_color = fill_color
        elif isinstance(fill_color, wagascianpy.plotting.colors.Colors):
            self._fill_color = fill_color.value
        elif isinstance(fill_color, string_types):
            self._fill_color = wagascianpy.plotting.fill_colors.Colors.get_by_detector(fill_color).value
        else:
            raise TypeError("fill color type is unknown {}".format(type(fill_color).__name__))

    @property
    def transparency(self):
        return self._transparency

    @transparency.setter
    def transparency(self, transparency):
        if not 0 < transparency < 1:
            raise ValueError("Transparence must be a percentage from zero to one")
        self._transparency = transparency

    def make_tobjects(self):
        left_markers = super(DoubleMarker, self).make_tobjects()
        right_markers = []
        y_minimum = ROOT.gPad.GetUymin()
        y_maximum = ROOT.gPad.GetUymax()
        x_minimum = ROOT.gPad.GetUxmin()
        x_maximum = ROOT.gPad.GetUxmax()
        tline = ROOT.TLine(self.right_position, y_minimum, self.right_position, y_maximum)
        tline.SetLineColor(self.line_color)
        tline.SetLineWidth(1)
        tline.SetLineStyle(2)
        if self.fill_color:
            tbox = ROOT.TBox(self.left_position, y_minimum, self.right_position, y_maximum)
            tbox.SetLineWidth(0)
            tbox.SetFillColorAlpha(self.fill_color + 1, self.transparency)
            right_markers.append(tbox)
        if self.right_text:
            ttext = ROOT.TText(self.right_position - (x_maximum - x_minimum) * 0.025,
                               0.98 * y_maximum, self.right_text)
            ttext.SetTextAngle(90)
            ttext.SetTextAlign(33)
            ttext.SetTextSize(0.03)
            ttext.SetTextColor(self.line_color)
            right_markers.append(ttext)
        right_markers.append(tline)
        return right_markers + left_markers


class CustomEvents(ABC):
    _custom_events = []
    _fill_color = ROOT.kGray

    def __init__(self, start, stop=None, wagasci_database=None):
        self._start = start
        self._stop = stop
        self._wagasci_database = wagasci_database

    def get_interval(self, include_overlapping=False):
        start = self._start
        stop = self._stop
        start, stop = wagascianpy.database.wagascidb.run_to_interval(start=start, stop=stop,
                                                                     database=self._wagasci_database)
        interval = []
        for custom_event in self._custom_events:
            start_time = wagascianpy.database.wagascidb.WagasciRunRecord.str2datetime(custom_event.start)
            stop_time = wagascianpy.database.wagascidb.WagasciRunRecord.str2datetime(custom_event.stop)
            if include_overlapping:
                if start < start_time < stop or start < stop_time < stop:
                    interval.append(custom_event)
            else:
                if start < start_time < stop and start < stop_time < stop:
                    interval.append(custom_event)
        return interval

    def get_markers(self, include_overlapping=False):
        days = self.get_interval(include_overlapping)
        markers = []
        for day in days:
            start_timestamp = wagascianpy.database.wagascidb.WagasciRunRecord.str2timestamp(day.start)
            stop_timestamp = wagascianpy.database.wagascidb.WagasciRunRecord.str2timestamp(day.stop)
            marker = DoubleMarker(left_position=start_timestamp, right_position=stop_timestamp,
                                  left_text="{} ({})".format(day.label, day.start))
            marker.line_color = wagascianpy.plotting.colors.Colors.Black
            marker.fill_color = self._fill_color
            marker.transparency = 0.2
            markers.append(marker)
        return markers


class MaintenanceDays(CustomEvents):
    _fill_color = wagascianpy.plotting.colors.Colors.Green
    _custom_events = [
        CustomEvent('2019/11/07 05:30:00', '2019/11/07 17:30:00', 12, 'half day maintenance'),
        CustomEvent('2019/11/13 09:00:00', '2019/11/14 09:00:00', 24, 'one day maintenance'),
        CustomEvent('2019/11/20 05:30:00', '2019/11/20 17:30:00', 12, 'half day maintenance'),
        CustomEvent('2019/11/27 09:00:00', '2019/11/28 09:00:00', 24, 'one day maintenance'),
        CustomEvent('2019/12/04 05:30:00', '2019/12/04 17:30:00', 12, 'half day maintenance'),
        CustomEvent('2019/12/11 09:00:00', '2019/12/12 09:00:00', 24, 'one day maintenance'),
        CustomEvent('2019/12/19 09:00:00', '2020/01/14 15:00:00', 630, 'end of year shutdown'),
        CustomEvent('2020/01/16 05:30:00', '2020/01/16 17:30:00', 12, 'half day maintenance'),
        CustomEvent('2020/01/22 09:00:00', '2020/01/23 09:00:00', 24, 'one day maintenance'),
        CustomEvent('2020/01/29 05:30:00', '2020/01/29 17:30:00', 12, 'half day maintenance'),
        CustomEvent('2020/02/05 09:00:00', '2020/02/06 09:00:00', 24, 'one day maintenance'),
        CustomEvent('2020/02/12 05:30:00', '2020/02/12 17:30:00', 12, 'half day maintenance'),
    ]


class TroubleEvents(CustomEvents):
    _fill_color = wagascianpy.plotting.colors.Colors.Red
    _custom_events = [
        CustomEvent('2020/02/11 12:52:32', '2020/02/11 22:30:32', 9.6333, 'WallMRD south data corruption'),
        CustomEvent('2020/02/02 10:47:03', '2020/02/02 18:51:20', 8.0666, 'WallMRD north data corruption'),
        CustomEvent('2020/02/04 09:04:39', '2020/02/04 14:07:09', 5.0416, 'WallMRD north data corruption'),
        CustomEvent('2020/01/31 09:56:07', '2020/01/31 14:35:42', 4.6597, 'WallMRD south data corruption'),
        CustomEvent('2020/01/30 22:19:00', '2020/01/30 22:48:00', 0.4833, 'WallMRD south HV failed'),
        CustomEvent('2020/01/30 12:52:00', '2020/01/30 13:48:00', 0.9333, 'WAGASCI downstream HV failed'),
        CustomEvent('2020/01/29 17:49:16', '2020/01/29 18:26:00', 0.6, 'WAGASCI run 91 : Data corruption'),
        CustomEvent('2020/01/24 16:09:35', '2020/01/24 16:26:44', 0.2833, 'WAGASCI run 82-83 : Data corruption'),
        CustomEvent('2020/01/21 11:02:00', '2020/01/21 15:45:00', 4.7166, 'WAGASCI run 73-77 : Data corruption'),
        CustomEvent('2020/01/20 19:51:24', '2020/01/21 14:22:05', 18.5, 'WAGASCI run 72 overwritten : human error'),
        # CustomEvent('2020/01/20 19:30:00', '2020/01/20 19:50:00', 0.3333, 'CCC trouble'),
        CustomEvent('2020/01/14 10:46:26', '2020/01/14 12:57:09', 1.1833, 'WAGASCI run 56-57 : Data corruption'),
        CustomEvent('2019/12/15 14:39:26', '2020/12/16 12:31:58', 21.866, 'WAGASCI run 43-48 : Data corruption'),
        CustomEvent('2019/11/26 04:03:02', '2019/11/27 09:00:00', 4.9494, 'WAGASCI run 26 : Data corruption'),
        CustomEvent('2019/11/18 14:51:19', '2019/11/18 18:22:16', 3.5158, 'WAGASCI downstream data corruption'),
        CustomEvent('2019/11/17 12:56:07', '2019/11/17 20:13:41', 7.2927, 'WAGASCI downstream data corruption'),
        CustomEvent('2019/11/11 07:04:45', '2019/11/11 11:39:58', 4.5869, 'WAGASCI upstream data corruption'),
        CustomEvent('2019/11/10 19:23:23', '2019/11/11 11:39:58', 16.2763, 'WAGASCI downstream data corruption'),
        CustomEvent('2019/11/08 17:39:19', '2019/11/09 19:53:00', 26.23, 'WAGASCI run 8 : Data corruption')
    ]
