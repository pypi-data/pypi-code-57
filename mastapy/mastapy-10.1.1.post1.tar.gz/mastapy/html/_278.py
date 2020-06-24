'''_278.py

HeadingType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_HEADING_TYPE = python_net_import('SMT.MastaAPI.HTML', 'HeadingType')


__docformat__ = 'restructuredtext en'
__all__ = ('HeadingType',)


class HeadingType(Enum):
    '''HeadingType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _HEADING_TYPE
    __hash__ = None

    VERY_SMALL = 0
    REGULAR = 1
    MEDIUM = 2
    LARGE = 3
