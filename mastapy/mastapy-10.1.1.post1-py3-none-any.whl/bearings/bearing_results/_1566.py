'''_1566.py

DefaultOrUserInput
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_DEFAULT_OR_USER_INPUT = python_net_import('SMT.MastaAPI.Bearings.BearingResults', 'DefaultOrUserInput')


__docformat__ = 'restructuredtext en'
__all__ = ('DefaultOrUserInput',)


class DefaultOrUserInput(Enum):
    '''DefaultOrUserInput

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _DEFAULT_OR_USER_INPUT

    __hash__ = None

    DIN_STANDARD_DEFAULT = 0
    USERSPECIFIED = 1
