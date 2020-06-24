'''_1394.py

CadTableBorderType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_CAD_TABLE_BORDER_TYPE = python_net_import('SMT.MastaAPI.Utility.Report', 'CadTableBorderType')


__docformat__ = 'restructuredtext en'
__all__ = ('CadTableBorderType',)


class CadTableBorderType(Enum):
    '''CadTableBorderType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _CAD_TABLE_BORDER_TYPE
    __hash__ = None

    SINGLE = 0
    DOUBLE = 1
