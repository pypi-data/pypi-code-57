'''_814.py

MicroGeometryProfileConvention
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_MICRO_GEOMETRY_PROFILE_CONVENTION = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'MicroGeometryProfileConvention')


__docformat__ = 'restructuredtext en'
__all__ = ('MicroGeometryProfileConvention',)


class MicroGeometryProfileConvention(Enum):
    '''MicroGeometryProfileConvention

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _MICRO_GEOMETRY_PROFILE_CONVENTION

    __hash__ = None

    MASTA_DEFAULT_MATERIAL = 0
    LDP = 1
    ISOAGMADIN = 2
    VDIVDE = 3
