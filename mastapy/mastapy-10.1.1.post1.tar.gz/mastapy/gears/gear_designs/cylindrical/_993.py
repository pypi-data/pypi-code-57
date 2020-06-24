'''_993.py

GeometrySpecificationType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_GEOMETRY_SPECIFICATION_TYPE = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'GeometrySpecificationType')


__docformat__ = 'restructuredtext en'
__all__ = ('GeometrySpecificationType',)


class GeometrySpecificationType(Enum):
    '''GeometrySpecificationType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _GEOMETRY_SPECIFICATION_TYPE
    __hash__ = None

    BASIC_RACK = 0
    PINION_TYPE_CUTTER = 1
    EXISTING_CUTTER_OBSOLETE = 2
    MANUFACTURING_CONFIGURATION = 3
