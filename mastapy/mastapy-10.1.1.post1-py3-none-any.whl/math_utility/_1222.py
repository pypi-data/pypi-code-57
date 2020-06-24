'''_1222.py

ExtrapolationOptions
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_EXTRAPOLATION_OPTIONS = python_net_import('SMT.MastaAPI.MathUtility', 'ExtrapolationOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('ExtrapolationOptions',)


class ExtrapolationOptions(Enum):
    '''ExtrapolationOptions

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _EXTRAPOLATION_OPTIONS
    __hash__ = None

    FLAT = 0
    LINEAR = 1
    THROW_EXCEPTION = 2
    WRAP = 3
