'''_664.py

CentreDistanceOffsetMethod
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_CENTRE_DISTANCE_OFFSET_METHOD = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew', 'CentreDistanceOffsetMethod')


__docformat__ = 'restructuredtext en'
__all__ = ('CentreDistanceOffsetMethod',)


class CentreDistanceOffsetMethod(Enum):
    '''CentreDistanceOffsetMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _CENTRE_DISTANCE_OFFSET_METHOD
    __hash__ = None

    CONSTANT_CENTRE_DISTANCE_OFFSET = 0
    PARABOLIC_CURVE_FOR_CENTRE_DISTANCE_OFFSET = 1
    SPECIFIED_GEAR_LEAD_MODIFICATION = 2
