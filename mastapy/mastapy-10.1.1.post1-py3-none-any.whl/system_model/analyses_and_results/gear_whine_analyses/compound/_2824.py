'''_2824.py

KlingelnbergCycloPalloidHypoidGearCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2021
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _3840
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _2822
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'KlingelnbergCycloPalloidHypoidGearCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearCompoundGearWhineAnalysis',)


class KlingelnbergCycloPalloidHypoidGearCompoundGearWhineAnalysis(_2822.KlingelnbergCycloPalloidConicalGearCompoundGearWhineAnalysis):
    '''KlingelnbergCycloPalloidHypoidGearCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_COMPOUND_GEAR_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2021.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2021.KlingelnbergCycloPalloidHypoidGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3840.KlingelnbergCycloPalloidHypoidGearGearWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3840.KlingelnbergCycloPalloidHypoidGearGearWhineAnalysis))
        return value

    @property
    def component_gear_whine_analysis_load_cases(self) -> 'List[_3840.KlingelnbergCycloPalloidHypoidGearGearWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearGearWhineAnalysis]: 'ComponentGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentGearWhineAnalysisLoadCases, constructor.new(_3840.KlingelnbergCycloPalloidHypoidGearGearWhineAnalysis))
        return value
