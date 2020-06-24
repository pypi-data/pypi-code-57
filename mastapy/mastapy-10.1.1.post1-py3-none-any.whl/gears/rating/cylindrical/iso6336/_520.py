'''_520.py

HelicalGearMicroGeometryOption
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_HELICAL_GEAR_MICRO_GEOMETRY_OPTION = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical.ISO6336', 'HelicalGearMicroGeometryOption')


__docformat__ = 'restructuredtext en'
__all__ = ('HelicalGearMicroGeometryOption',)


class HelicalGearMicroGeometryOption(Enum):
    '''HelicalGearMicroGeometryOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _HELICAL_GEAR_MICRO_GEOMETRY_OPTION
    __hash__ = None

    SUITABLE = 0
    BASED_ON_PRACTICAL_EXPERIENCE = 1
    NONE = 2
