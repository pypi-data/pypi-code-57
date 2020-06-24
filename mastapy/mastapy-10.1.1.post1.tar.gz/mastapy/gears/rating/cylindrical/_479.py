'''_479.py

CylindricalGearRatingGeometryDataSource
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_RATING_GEOMETRY_DATA_SOURCE = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical', 'CylindricalGearRatingGeometryDataSource')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearRatingGeometryDataSource',)


class CylindricalGearRatingGeometryDataSource(Enum):
    '''CylindricalGearRatingGeometryDataSource

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _CYLINDRICAL_GEAR_RATING_GEOMETRY_DATA_SOURCE
    __hash__ = None

    BASIC_RACK = 0
    PINION_TYPE_CUTTER = 1
    MANUFACTURING_CONFIGURATION = 2
    ROUGH_MANUFACTURING_CONFIGURATION = 3
