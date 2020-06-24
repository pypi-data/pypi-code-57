'''_1114.py

WheelFinishCutterPointWidthRestrictionMethod
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_WHEEL_FINISH_CUTTER_POINT_WIDTH_RESTRICTION_METHOD = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Bevel', 'WheelFinishCutterPointWidthRestrictionMethod')


__docformat__ = 'restructuredtext en'
__all__ = ('WheelFinishCutterPointWidthRestrictionMethod',)


class WheelFinishCutterPointWidthRestrictionMethod(Enum):
    '''WheelFinishCutterPointWidthRestrictionMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _WHEEL_FINISH_CUTTER_POINT_WIDTH_RESTRICTION_METHOD
    __hash__ = None

    NONE = 0
    TO_NEAREST_01_MM = 1
    TO_NEAREST_0005_INCHES = 2
