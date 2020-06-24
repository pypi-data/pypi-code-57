'''_1392.py

CadPageOrientation
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_CAD_PAGE_ORIENTATION = python_net_import('SMT.MastaAPI.Utility.Report', 'CadPageOrientation')


__docformat__ = 'restructuredtext en'
__all__ = ('CadPageOrientation',)


class CadPageOrientation(Enum):
    '''CadPageOrientation

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _CAD_PAGE_ORIENTATION
    __hash__ = None

    LANDSCAPE = 0
    PORTRAIT = 1
