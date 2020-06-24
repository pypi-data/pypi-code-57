'''_2117.py

CompoundDynamicModelforatSpeedsAnalysis
'''


from mastapy.system_model.analyses_and_results import _2080
from mastapy._internal.python_net import python_net_import

_COMPOUND_DYNAMIC_MODELFORAT_SPEEDS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'CompoundDynamicModelforatSpeedsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CompoundDynamicModelforatSpeedsAnalysis',)


class CompoundDynamicModelforatSpeedsAnalysis(_2080.CompoundAnalysis):
    '''CompoundDynamicModelforatSpeedsAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPOUND_DYNAMIC_MODELFORAT_SPEEDS_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CompoundDynamicModelforatSpeedsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
