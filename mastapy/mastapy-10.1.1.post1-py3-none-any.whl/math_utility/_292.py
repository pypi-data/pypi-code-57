'''_292.py

Axis
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_AXIS = python_net_import('SMT.MastaAPI.MathUtility', 'Axis')


__docformat__ = 'restructuredtext en'
__all__ = ('Axis',)


class Axis(Enum):
    '''Axis

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _AXIS
    __hash__ = None

    X = 0
    Y = 1
    Z = 2
