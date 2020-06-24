'''_920.py

LargerOrSmaller
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_LARGER_OR_SMALLER = python_net_import('SMT.MastaAPI.Gears.GearSetParetoOptimiser', 'LargerOrSmaller')


__docformat__ = 'restructuredtext en'
__all__ = ('LargerOrSmaller',)


class LargerOrSmaller(Enum):
    '''LargerOrSmaller

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _LARGER_OR_SMALLER
    __hash__ = None

    LARGER_VALUES = 0
    SMALLER_VALUES = 1
