'''_429.py

MicroGeometryDefinitionMethod
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_MICRO_GEOMETRY_DEFINITION_METHOD = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.PlungeShaving', 'MicroGeometryDefinitionMethod')


__docformat__ = 'restructuredtext en'
__all__ = ('MicroGeometryDefinitionMethod',)


class MicroGeometryDefinitionMethod(Enum):
    '''MicroGeometryDefinitionMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _MICRO_GEOMETRY_DEFINITION_METHOD

    __hash__ = None

    NORMAL_TO_INVOLUTE = 0
    ARC_LENGTH = 1
