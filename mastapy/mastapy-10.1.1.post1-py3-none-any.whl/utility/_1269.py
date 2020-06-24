'''_1269.py

LoadCaseOverrideOption
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_LOAD_CASE_OVERRIDE_OPTION = python_net_import('SMT.MastaAPI.Utility', 'LoadCaseOverrideOption')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadCaseOverrideOption',)


class LoadCaseOverrideOption(Enum):
    '''LoadCaseOverrideOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _LOAD_CASE_OVERRIDE_OPTION
    __hash__ = None

    LOAD_CASE_SETTING = 0
    YES = 1
    NO = 2
