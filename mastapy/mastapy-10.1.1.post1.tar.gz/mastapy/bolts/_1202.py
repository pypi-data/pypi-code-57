'''_1202.py

HeadCapTypes
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_HEAD_CAP_TYPES = python_net_import('SMT.MastaAPI.Bolts', 'HeadCapTypes')


__docformat__ = 'restructuredtext en'
__all__ = ('HeadCapTypes',)


class HeadCapTypes(Enum):
    '''HeadCapTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _HEAD_CAP_TYPES
    __hash__ = None

    HEXAGONAL_HEAD = 0
    SOCKET_HEAD = 1
