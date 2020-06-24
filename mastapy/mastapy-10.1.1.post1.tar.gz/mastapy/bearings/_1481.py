'''_1481.py

RollingBearingArrangement
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_ROLLING_BEARING_ARRANGEMENT = python_net_import('SMT.MastaAPI.Bearings', 'RollingBearingArrangement')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingBearingArrangement',)


class RollingBearingArrangement(Enum):
    '''RollingBearingArrangement

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _ROLLING_BEARING_ARRANGEMENT
    __hash__ = None

    SINGLE = 0
    TANDEM = 1
    PAIR_X = 2
    PAIR_O = 3
    DOUBLE = 4
