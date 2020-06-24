'''_2587.py

StraightBevelGearCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2015
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _3731
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _2565
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'StraightBevelGearCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearCompoundDynamicAnalysis',)


class StraightBevelGearCompoundDynamicAnalysis(_2565.BevelGearCompoundDynamicAnalysis):
    '''StraightBevelGearCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_COMPOUND_DYNAMIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2015.StraightBevelGear':
        '''StraightBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2015.StraightBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3731.StraightBevelGearDynamicAnalysis]':
        '''List[StraightBevelGearDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3731.StraightBevelGearDynamicAnalysis))
        return value

    @property
    def component_dynamic_analysis_load_cases(self) -> 'List[_3731.StraightBevelGearDynamicAnalysis]':
        '''List[StraightBevelGearDynamicAnalysis]: 'ComponentDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentDynamicAnalysisLoadCases, constructor.new(_3731.StraightBevelGearDynamicAnalysis))
        return value
