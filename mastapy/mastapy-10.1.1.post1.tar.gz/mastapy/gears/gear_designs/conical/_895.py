'''_895.py

CutterBladeType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_CUTTER_BLADE_TYPE = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Conical', 'CutterBladeType')


__docformat__ = 'restructuredtext en'
__all__ = ('CutterBladeType',)


class CutterBladeType(Enum):
    '''CutterBladeType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _CUTTER_BLADE_TYPE

    __hash__ = None

    STRAIGHT = 0
    CIRCULAR_ARC = 1
    PARABOLIC = 2
