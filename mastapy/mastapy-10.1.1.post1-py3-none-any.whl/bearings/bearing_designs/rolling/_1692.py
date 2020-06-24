'''_1692.py

DiameterSeries
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_DIAMETER_SERIES = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling', 'DiameterSeries')


__docformat__ = 'restructuredtext en'
__all__ = ('DiameterSeries',)


class DiameterSeries(Enum):
    '''DiameterSeries

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _DIAMETER_SERIES
    __hash__ = None

    _0 = 0
    _1 = 1
    _2 = 2
    _3 = 3
    _4 = 4
    _5 = 5
    _7 = 7
    _8 = 8
    _9 = 9
