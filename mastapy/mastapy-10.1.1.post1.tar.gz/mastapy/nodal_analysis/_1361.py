'''_1361.py

BarModelAnalysisType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_BAR_MODEL_ANALYSIS_TYPE = python_net_import('SMT.MastaAPI.NodalAnalysis', 'BarModelAnalysisType')


__docformat__ = 'restructuredtext en'
__all__ = ('BarModelAnalysisType',)


class BarModelAnalysisType(Enum):
    '''BarModelAnalysisType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _BAR_MODEL_ANALYSIS_TYPE

    __hash__ = None

    STATIC = 0
    DYNAMIC = 1
