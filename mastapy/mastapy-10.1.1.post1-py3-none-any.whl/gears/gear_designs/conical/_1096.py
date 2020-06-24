'''_1096.py

FrontEndTypes
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_FRONT_END_TYPES = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Conical', 'FrontEndTypes')


__docformat__ = 'restructuredtext en'
__all__ = ('FrontEndTypes',)


class FrontEndTypes(Enum):
    '''FrontEndTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _FRONT_END_TYPES
    __hash__ = None

    FLAT = 0
    CONICAL = 1
