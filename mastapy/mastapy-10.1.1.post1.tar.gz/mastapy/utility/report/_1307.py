'''_1307.py

HeadingSize
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_HEADING_SIZE = python_net_import('SMT.MastaAPI.Utility.Report', 'HeadingSize')


__docformat__ = 'restructuredtext en'
__all__ = ('HeadingSize',)


class HeadingSize(Enum):
    '''HeadingSize

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _HEADING_SIZE

    __hash__ = None

    REGULAR = 0
    MEDIUM = 1
    LARGE = 2
