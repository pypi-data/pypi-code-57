'''_1751.py

HeightSeries
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_HEIGHT_SERIES = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling', 'HeightSeries')


__docformat__ = 'restructuredtext en'
__all__ = ('HeightSeries',)


class HeightSeries(Enum):
    '''HeightSeries

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _HEIGHT_SERIES

    __hash__ = None

    _1 = 1
    _7 = 7
    _9 = 9
