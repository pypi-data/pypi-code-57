'''_270.py

DynamicFactorMethods
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_DYNAMIC_FACTOR_METHODS = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical', 'DynamicFactorMethods')


__docformat__ = 'restructuredtext en'
__all__ = ('DynamicFactorMethods',)


class DynamicFactorMethods(Enum):
    '''DynamicFactorMethods

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _DYNAMIC_FACTOR_METHODS

    __hash__ = None

    METHOD_B = 0
    METHOD_C = 1
    SELECT_AUTOMATICALLY = 2
