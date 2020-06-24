'''_813.py

MicroGeometryConvention
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_MICRO_GEOMETRY_CONVENTION = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'MicroGeometryConvention')


__docformat__ = 'restructuredtext en'
__all__ = ('MicroGeometryConvention',)


class MicroGeometryConvention(Enum):
    '''MicroGeometryConvention

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _MICRO_GEOMETRY_CONVENTION

    __hash__ = None

    MASTA_DEFAULT_MATERIAL = 0
    LDP = 1
    ISOAGMADINVDIVDE = 2
