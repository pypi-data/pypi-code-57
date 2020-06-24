'''_2895.py

SpiralBevelGearSetCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _1966
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _2894, _2953, _2877
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _3846
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_SET_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'SpiralBevelGearSetCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearSetCompoundGearWhineAnalysis',)


class SpiralBevelGearSetCompoundGearWhineAnalysis(_2877.BevelGearSetCompoundGearWhineAnalysis):
    '''SpiralBevelGearSetCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_SET_COMPOUND_GEAR_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearSetCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1966.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1966.SpiralBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1966.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1966.SpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def spiral_bevel_gears_compound_gear_whine_analysis(self) -> 'List[_2894.SpiralBevelGearCompoundGearWhineAnalysis]':
        '''List[SpiralBevelGearCompoundGearWhineAnalysis]: 'SpiralBevelGearsCompoundGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearsCompoundGearWhineAnalysis, constructor.new(_2894.SpiralBevelGearCompoundGearWhineAnalysis))
        return value

    @property
    def spiral_bevel_meshes_compound_gear_whine_analysis(self) -> 'List[_2953.SpiralBevelGearMeshCompoundGearWhineAnalysis]':
        '''List[SpiralBevelGearMeshCompoundGearWhineAnalysis]: 'SpiralBevelMeshesCompoundGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelMeshesCompoundGearWhineAnalysis, constructor.new(_2953.SpiralBevelGearMeshCompoundGearWhineAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_3846.SpiralBevelGearSetGearWhineAnalysis]':
        '''List[SpiralBevelGearSetGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3846.SpiralBevelGearSetGearWhineAnalysis))
        return value

    @property
    def assembly_gear_whine_analysis_load_cases(self) -> 'List[_3846.SpiralBevelGearSetGearWhineAnalysis]':
        '''List[SpiralBevelGearSetGearWhineAnalysis]: 'AssemblyGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyGearWhineAnalysisLoadCases, constructor.new(_3846.SpiralBevelGearSetGearWhineAnalysis))
        return value
