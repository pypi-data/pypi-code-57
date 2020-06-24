'''_828.py

ThicknessType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_THICKNESS_TYPE = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'ThicknessType')


__docformat__ = 'restructuredtext en'
__all__ = ('ThicknessType',)


class ThicknessType(Enum):
    '''ThicknessType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _THICKNESS_TYPE

    __hash__ = None

    UNSPECIFIED = 0
    NORMAL_THICKNESS = 1
    CHORDAL_SPAN = 2
    OVER_BALLS = 3
    TRANSVERSE_THICKNESS = 4
    PROFILE_SHIFT = 5
    NORMAL_THICKNESS_AT_DIAMETER = 6
    TRANSVERSE_THICKNESS_AT_DIAMETER = 7
    PROFILE_SHIFT_COEFFICIENT = 8
    CALCULATED = -2
    SPECIFICATION_FROM_STANDARD = -1
