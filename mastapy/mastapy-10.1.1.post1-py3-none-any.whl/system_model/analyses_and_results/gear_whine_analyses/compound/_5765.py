'''_5765.py

StraightBevelGearCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2086
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5376
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5679
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'StraightBevelGearCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearCompoundGearWhineAnalysis',)


class StraightBevelGearCompoundGearWhineAnalysis(_5679.BevelGearCompoundGearWhineAnalysis):
    '''StraightBevelGearCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2086.StraightBevelGear':
        '''StraightBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2086.StraightBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5376.StraightBevelGearGearWhineAnalysis]':
        '''List[StraightBevelGearGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5376.StraightBevelGearGearWhineAnalysis))
        return value

    @property
    def component_gear_whine_analysis_load_cases(self) -> 'List[_5376.StraightBevelGearGearWhineAnalysis]':
        '''List[StraightBevelGearGearWhineAnalysis]: 'ComponentGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentGearWhineAnalysisLoadCases, constructor.new(_5376.StraightBevelGearGearWhineAnalysis))
        return value
