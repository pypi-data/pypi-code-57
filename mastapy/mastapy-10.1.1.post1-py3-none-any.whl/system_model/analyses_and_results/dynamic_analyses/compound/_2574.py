'''_2574.py

HypoidGearCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2011
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _3718
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _2559
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'HypoidGearCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearCompoundDynamicAnalysis',)


class HypoidGearCompoundDynamicAnalysis(_2559.AGMAGleasonConicalGearCompoundDynamicAnalysis):
    '''HypoidGearCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_COMPOUND_DYNAMIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2011.HypoidGear':
        '''HypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2011.HypoidGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3718.HypoidGearDynamicAnalysis]':
        '''List[HypoidGearDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3718.HypoidGearDynamicAnalysis))
        return value

    @property
    def component_dynamic_analysis_load_cases(self) -> 'List[_3718.HypoidGearDynamicAnalysis]':
        '''List[HypoidGearDynamicAnalysis]: 'ComponentDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentDynamicAnalysisLoadCases, constructor.new(_3718.HypoidGearDynamicAnalysis))
        return value
