'''_90.py

FENodeOption
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_FE_NODE_OPTION = python_net_import('SMT.MastaAPI.NodalAnalysis', 'FENodeOption')


__docformat__ = 'restructuredtext en'
__all__ = ('FENodeOption',)


class FENodeOption(Enum):
    '''FENodeOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _FE_NODE_OPTION
    __hash__ = None

    NONE = 0
    SURFACE = 1
    ALL = 2
