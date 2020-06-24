'''_501.py

ScuffingMethods
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_SCUFFING_METHODS = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical', 'ScuffingMethods')


__docformat__ = 'restructuredtext en'
__all__ = ('ScuffingMethods',)


class ScuffingMethods(Enum):
    '''ScuffingMethods

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _SCUFFING_METHODS
    __hash__ = None

    AGMA_2001B88_OLD = 0
    AGMA_925A03_NEW = 1
