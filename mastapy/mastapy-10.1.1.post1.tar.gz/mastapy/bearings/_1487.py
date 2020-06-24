'''_1487.py

TiltingPadTypes
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_TILTING_PAD_TYPES = python_net_import('SMT.MastaAPI.Bearings', 'TiltingPadTypes')


__docformat__ = 'restructuredtext en'
__all__ = ('TiltingPadTypes',)


class TiltingPadTypes(Enum):
    '''TiltingPadTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _TILTING_PAD_TYPES
    __hash__ = None

    NONEQUALISED = 0
    EQUALISED = 1
