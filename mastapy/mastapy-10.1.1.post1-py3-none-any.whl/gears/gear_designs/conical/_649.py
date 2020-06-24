'''_649.py

ConicalFlanks
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_CONICAL_FLANKS = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Conical', 'ConicalFlanks')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalFlanks',)


class ConicalFlanks(Enum):
    '''ConicalFlanks

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _CONICAL_FLANKS
    __hash__ = None

    CONCAVE = 0
    CONVEX = 1
    WORST = 2
