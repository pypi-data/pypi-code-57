'''_308.py

MicroGeometryInputTypes
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_MICRO_GEOMETRY_INPUT_TYPES = python_net_import('SMT.MastaAPI.Gears', 'MicroGeometryInputTypes')


__docformat__ = 'restructuredtext en'
__all__ = ('MicroGeometryInputTypes',)


class MicroGeometryInputTypes(Enum):
    '''MicroGeometryInputTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _MICRO_GEOMETRY_INPUT_TYPES
    __hash__ = None

    FACTORS = 0
    MEASUREMENTS = 1
