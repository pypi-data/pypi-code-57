'''_1310.py

Severity
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_SEVERITY = python_net_import('SMT.MastaAPI.Utility.ModelValidation', 'Severity')


__docformat__ = 'restructuredtext en'
__all__ = ('Severity',)


class Severity(Enum):
    '''Severity

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _SEVERITY

    __hash__ = None

    INFORMATION = 1
    WARNING = 2
    ERROR = 3
