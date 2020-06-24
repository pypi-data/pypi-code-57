'''_1196.py

BoltShankType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_BOLT_SHANK_TYPE = python_net_import('SMT.MastaAPI.Bolts', 'BoltShankType')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltShankType',)


class BoltShankType(Enum):
    '''BoltShankType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _BOLT_SHANK_TYPE
    __hash__ = None

    SHANKED = 0
    NECKED_DOWN = 1
