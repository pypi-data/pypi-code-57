'''_2832.py

StraightBevelDiffGearSetCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _1989
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _2831, _2879, _2812
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _3848
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'StraightBevelDiffGearSetCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetCompoundGearWhineAnalysis',)


class StraightBevelDiffGearSetCompoundGearWhineAnalysis(_2812.BevelGearSetCompoundGearWhineAnalysis):
    '''StraightBevelDiffGearSetCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_COMPOUND_GEAR_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1989.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1989.StraightBevelDiffGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1989.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1989.StraightBevelDiffGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def straight_bevel_diff_gears_compound_gear_whine_analysis(self) -> 'List[_2831.StraightBevelDiffGearCompoundGearWhineAnalysis]':
        '''List[StraightBevelDiffGearCompoundGearWhineAnalysis]: 'StraightBevelDiffGearsCompoundGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearsCompoundGearWhineAnalysis, constructor.new(_2831.StraightBevelDiffGearCompoundGearWhineAnalysis))
        return value

    @property
    def straight_bevel_diff_meshes_compound_gear_whine_analysis(self) -> 'List[_2879.StraightBevelDiffGearMeshCompoundGearWhineAnalysis]':
        '''List[StraightBevelDiffGearMeshCompoundGearWhineAnalysis]: 'StraightBevelDiffMeshesCompoundGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshesCompoundGearWhineAnalysis, constructor.new(_2879.StraightBevelDiffGearMeshCompoundGearWhineAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_3848.StraightBevelDiffGearSetGearWhineAnalysis]':
        '''List[StraightBevelDiffGearSetGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3848.StraightBevelDiffGearSetGearWhineAnalysis))
        return value

    @property
    def assembly_gear_whine_analysis_load_cases(self) -> 'List[_3848.StraightBevelDiffGearSetGearWhineAnalysis]':
        '''List[StraightBevelDiffGearSetGearWhineAnalysis]: 'AssemblyGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyGearWhineAnalysisLoadCases, constructor.new(_3848.StraightBevelDiffGearSetGearWhineAnalysis))
        return value
