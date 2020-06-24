'''_919.py

EdgeRadiusType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_EDGE_RADIUS_TYPE = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Bevel', 'EdgeRadiusType')


__docformat__ = 'restructuredtext en'
__all__ = ('EdgeRadiusType',)


class EdgeRadiusType(Enum):
    '''EdgeRadiusType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _EDGE_RADIUS_TYPE

    __hash__ = None

    USERSPECIFIED = 0
    CALCULATED_MAXIMUM = 1
