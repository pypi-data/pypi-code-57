'''_1388.py

SectionEnd
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_SECTION_END = python_net_import('SMT.MastaAPI.NodalAnalysis', 'SectionEnd')


__docformat__ = 'restructuredtext en'
__all__ = ('SectionEnd',)


class SectionEnd(Enum):
    '''SectionEnd

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _SECTION_END

    __hash__ = None

    LEFT = 0
    RIGHT = 1
