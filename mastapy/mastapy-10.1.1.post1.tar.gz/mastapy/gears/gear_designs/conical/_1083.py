'''_1083.py

KlingelnbergFinishingMethods
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_FINISHING_METHODS = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Conical', 'KlingelnbergFinishingMethods')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergFinishingMethods',)


class KlingelnbergFinishingMethods(Enum):
    '''KlingelnbergFinishingMethods

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _KLINGELNBERG_FINISHING_METHODS
    __hash__ = None

    LAPPED = 0
    SOFTCUT = 1
    HPG = 2
