# Copyright 2019 Cognite AS

import itertools
from enum import Enum

import numpy as np

from cognite.seismic.data_classes.custom_list import CustomList

TRACE_HEADER_SIZE = 240


class TraceField(Enum):
    """
    Trace header field enumerator
    """

    SourceGroupScalar = 70
    CDP_X = 180
    CDP_Y = 184
    INLINE_3D = 188
    CROSSLINE_3D = 192


def _read_header_short(trace_header, ie):
    i = ie.value
    return int.from_bytes(trace_header[i : i + 2], byteorder="big", signed=True)


def _read_header_int(trace_header, ie):
    i = ie.value
    return int.from_bytes(trace_header[i : i + 4], byteorder="big", signed=True)


class Trace:
    def __init__(self, trace):
        self.__trace = trace

    def __getitem__(self, item):
        return self.__trace[item]

    def __getattr__(self, item):
        return getattr(self.__trace, item)

    def __repr__(self):
        return repr(self.__trace)

    def _check_headers(self):
        if len(self.__trace.trace_header) != TRACE_HEADER_SIZE:
            raise ValueError("Header not requested")

    def get_source_group_scalar(self):
        self._check_headers()
        return _read_header_short(self.__trace.trace_header, TraceField.SourceGroupScalar)

    def get_x(self):
        self._check_headers()
        x = float(_read_header_int(self.__trace.trace_header, TraceField.CDP_X))
        scale_factor = self.get_source_group_scalar()
        if scale_factor > 0:
            x = x * scale_factor
        elif scale_factor < 0:
            x = x / -scale_factor
        return x

    def get_y(self):
        self._check_headers()
        y = float(_read_header_int(self.__trace.trace_header, TraceField.CDP_Y))
        scale_factor = self.get_source_group_scalar()
        if scale_factor > 0:
            y = y * scale_factor
        elif scale_factor < 0:
            y = y / -scale_factor
        return y

    def get_inline(self):
        self._check_headers()
        return _read_header_int(self.__trace.trace_header, TraceField.INLINE_3D)

    def get_xline(self):
        self._check_headers()
        return _read_header_int(self.__trace.trace_header, TraceField.CROSSLINE_3D)


class TraceIteratorWrapper:
    def __init__(self, it):
        self.it = it

    def __iter__(self):
        return self

    def __next__(self):
        return Trace(self.it.__next__())


class Trace3DList(CustomList):
    def __init__(self, iterable):
        super(Trace3DList, self).__init__(TraceIteratorWrapper(iterable))

    def to_array(self):
        group_list = self._group_by_inline()
        result = []
        for inline_group in group_list:
            result.append(np.array([np.array(i.trace) for i in inline_group]))
        return np.array(result)

    def xy_array(self):
        group_list = self._group_by_inline()
        result = []
        for inline_group in group_list:
            result.append(np.array([np.array([i.get_x(), i.get_y()]) for i in inline_group]))
        return np.array(result)

    def _group_by_inline(self):
        return [list(g) for k, g in itertools.groupby(self.to_list(), lambda x: x.iline.value)]


class Trace2DList(CustomList):
    def __init__(self, iterable):
        super(Trace2DList, self).__init__(TraceIteratorWrapper(iterable))

    def to_array(self):
        return np.array([np.array(t.trace) for t in self.to_list()])

    def xy_array(self):
        return np.array([np.array([t.get_x(), t.get_y()]) for t in self.to_list()])
