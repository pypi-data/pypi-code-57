'''_309.py

MicroGeometryModel
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_MICRO_GEOMETRY_MODEL = python_net_import('SMT.MastaAPI.Gears', 'MicroGeometryModel')


__docformat__ = 'restructuredtext en'
__all__ = ('MicroGeometryModel',)


class MicroGeometryModel(Enum):
    '''MicroGeometryModel

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _MICRO_GEOMETRY_MODEL
    __hash__ = None

    NONE = 0
    ESTIMATED_FROM_MACRO_GEOMETRY = 1
    SPECIFIED_MICRO_GEOMETRY = 2
