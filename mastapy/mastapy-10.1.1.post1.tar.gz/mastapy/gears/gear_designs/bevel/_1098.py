'''_1098.py

AGMAGleasonConicalGearGeometryMethods
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_AGMA_GLEASON_CONICAL_GEAR_GEOMETRY_METHODS = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Bevel', 'AGMAGleasonConicalGearGeometryMethods')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMAGleasonConicalGearGeometryMethods',)


class AGMAGleasonConicalGearGeometryMethods(Enum):
    '''AGMAGleasonConicalGearGeometryMethods

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _AGMA_GLEASON_CONICAL_GEAR_GEOMETRY_METHODS
    __hash__ = None

    GLEASON = 0
    AGMA_2005D03 = 1
    GLEASON_CAGE = 2
    GLEASON_GEMS = 3
    KIMOS = 4
