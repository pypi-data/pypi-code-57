'''_1272.py

RoundingMethods
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_ROUNDING_METHODS = python_net_import('SMT.MastaAPI.Utility', 'RoundingMethods')


__docformat__ = 'restructuredtext en'
__all__ = ('RoundingMethods',)


class RoundingMethods(Enum):
    '''RoundingMethods

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _ROUNDING_METHODS
    __hash__ = None

    AUTO = 0
    SIGNIFICANT_FIGURES = 1
    DECIMAL_PLACES = 2
