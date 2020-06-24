'''_797.py

DIN3967AllowanceSeries
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_DIN3967_ALLOWANCE_SERIES = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'DIN3967AllowanceSeries')


__docformat__ = 'restructuredtext en'
__all__ = ('DIN3967AllowanceSeries',)


class DIN3967AllowanceSeries(Enum):
    '''DIN3967AllowanceSeries

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _DIN3967_ALLOWANCE_SERIES

    __hash__ = None

    A = 0
    AB = 1
    B = 2
    BC = 3
    C = 4
    CD = 5
    D = 6
    E = 7
    F = 8
    G = 9
    H = 10
