'''_1102.py

StatusItemSeverity
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_STATUS_ITEM_SEVERITY = python_net_import('SMT.MastaAPI.Utility.ModelValidation', 'StatusItemSeverity')


__docformat__ = 'restructuredtext en'
__all__ = ('StatusItemSeverity',)


class StatusItemSeverity(Enum):
    '''StatusItemSeverity

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _STATUS_ITEM_SEVERITY
    __hash__ = None

    HEADER = 1
    INFORMATION = 16
    WARNING = 256
    ERROR = 4096
