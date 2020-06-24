'''_295.py

CylindricalFlanks
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_FLANKS = python_net_import('SMT.MastaAPI.Gears', 'CylindricalFlanks')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalFlanks',)


class CylindricalFlanks(Enum):
    '''CylindricalFlanks

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _CYLINDRICAL_FLANKS
    __hash__ = None

    LEFT = 0
    RIGHT = 1
    WORST = 2
