'''_6243.py

CombinationAnalysis
'''


from mastapy import _1
from mastapy._internal.python_net import python_net_import

_COMBINATION_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.FlexiblePinAnalyses', 'CombinationAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CombinationAnalysis',)


class CombinationAnalysis(_1.APIBase):
    '''CombinationAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMBINATION_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CombinationAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
