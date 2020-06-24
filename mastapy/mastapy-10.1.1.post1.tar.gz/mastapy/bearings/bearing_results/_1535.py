'''_1535.py

RaceAxialMountingType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_RACE_AXIAL_MOUNTING_TYPE = python_net_import('SMT.MastaAPI.Bearings.BearingResults', 'RaceAxialMountingType')


__docformat__ = 'restructuredtext en'
__all__ = ('RaceAxialMountingType',)


class RaceAxialMountingType(Enum):
    '''RaceAxialMountingType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _RACE_AXIAL_MOUNTING_TYPE
    __hash__ = None

    BOTH = 0
    LEFT = 1
    RIGHT = 2
    NONE = 3
