'''_196.py

NoneSelectedAllOption
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_NONE_SELECTED_ALL_OPTION = python_net_import('SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses', 'NoneSelectedAllOption')


__docformat__ = 'restructuredtext en'
__all__ = ('NoneSelectedAllOption',)


class NoneSelectedAllOption(Enum):
    '''NoneSelectedAllOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _NONE_SELECTED_ALL_OPTION
    __hash__ = None

    NONE = 0
    SELECTED = 1
    ALL = 2
