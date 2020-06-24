'''_1702.py

WidthSeries
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_WIDTH_SERIES = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling', 'WidthSeries')


__docformat__ = 'restructuredtext en'
__all__ = ('WidthSeries',)


class WidthSeries(Enum):
    '''WidthSeries

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _WIDTH_SERIES
    __hash__ = None

    _0 = 0
    _1 = 1
    _2 = 2
    _3 = 3
    _4 = 4
    _5 = 5
    _6 = 6
    _7 = 7
    _8 = 8
    _9 = 9
