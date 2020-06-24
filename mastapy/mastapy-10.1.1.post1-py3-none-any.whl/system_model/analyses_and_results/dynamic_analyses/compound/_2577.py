'''_2577.py

KlingelnbergCycloPalloidConicalGearSetCompoundDynamicAnalysis
'''


from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _2568
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'KlingelnbergCycloPalloidConicalGearSetCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidConicalGearSetCompoundDynamicAnalysis',)


class KlingelnbergCycloPalloidConicalGearSetCompoundDynamicAnalysis(_2568.ConicalGearSetCompoundDynamicAnalysis):
    '''KlingelnbergCycloPalloidConicalGearSetCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET_COMPOUND_DYNAMIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidConicalGearSetCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
