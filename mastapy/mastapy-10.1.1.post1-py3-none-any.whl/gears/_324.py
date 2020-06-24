'''_324.py

WormAddendumFactor
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_WORM_ADDENDUM_FACTOR = python_net_import('SMT.MastaAPI.Gears', 'WormAddendumFactor')


__docformat__ = 'restructuredtext en'
__all__ = ('WormAddendumFactor',)


class WormAddendumFactor(Enum):
    '''WormAddendumFactor

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _WORM_ADDENDUM_FACTOR
    __hash__ = None

    NORMAL = 0
    STUB = 1
