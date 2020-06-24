'''_124.py

SinglePointSelectionMethod
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_SINGLE_POINT_SELECTION_METHOD = python_net_import('SMT.MastaAPI.NodalAnalysis.VaryingInputComponents', 'SinglePointSelectionMethod')


__docformat__ = 'restructuredtext en'
__all__ = ('SinglePointSelectionMethod',)


class SinglePointSelectionMethod(Enum):
    '''SinglePointSelectionMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _SINGLE_POINT_SELECTION_METHOD
    __hash__ = None

    CURRENT_TIME = 0
    MEAN_VALUE = 1
