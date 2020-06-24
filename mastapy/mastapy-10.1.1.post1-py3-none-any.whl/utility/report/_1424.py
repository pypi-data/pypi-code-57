'''_1424.py

FontStyle
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_FONT_STYLE = python_net_import('SMT.MastaAPI.Utility.Report', 'FontStyle')


__docformat__ = 'restructuredtext en'
__all__ = ('FontStyle',)


class FontStyle(Enum):
    '''FontStyle

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _FONT_STYLE
    __hash__ = None

    NORMAL = 0
    ITALIC = 1
