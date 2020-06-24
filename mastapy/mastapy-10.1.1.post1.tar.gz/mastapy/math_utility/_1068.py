'''_1068.py

DegreesOfFreedom
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_DEGREES_OF_FREEDOM = python_net_import('SMT.MastaAPI.MathUtility', 'DegreesOfFreedom')


__docformat__ = 'restructuredtext en'
__all__ = ('DegreesOfFreedom',)


class DegreesOfFreedom(Enum):
    '''DegreesOfFreedom

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _DEGREES_OF_FREEDOM

    __hash__ = None

    X = 0
    Y = 1
    Z = 2
    ΘX = 3
    ΘY = 4
    ΘZ = 5
