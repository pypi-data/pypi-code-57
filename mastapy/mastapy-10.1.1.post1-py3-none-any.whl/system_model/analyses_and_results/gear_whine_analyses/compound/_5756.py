'''_5756.py

SpiralBevelGearCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2082
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5367
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5679
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'SpiralBevelGearCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearCompoundGearWhineAnalysis',)


class SpiralBevelGearCompoundGearWhineAnalysis(_5679.BevelGearCompoundGearWhineAnalysis):
    '''SpiralBevelGearCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2082.SpiralBevelGear':
        '''SpiralBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2082.SpiralBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5367.SpiralBevelGearGearWhineAnalysis]':
        '''List[SpiralBevelGearGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5367.SpiralBevelGearGearWhineAnalysis))
        return value

    @property
    def component_gear_whine_analysis_load_cases(self) -> 'List[_5367.SpiralBevelGearGearWhineAnalysis]':
        '''List[SpiralBevelGearGearWhineAnalysis]: 'ComponentGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentGearWhineAnalysisLoadCases, constructor.new(_5367.SpiralBevelGearGearWhineAnalysis))
        return value
