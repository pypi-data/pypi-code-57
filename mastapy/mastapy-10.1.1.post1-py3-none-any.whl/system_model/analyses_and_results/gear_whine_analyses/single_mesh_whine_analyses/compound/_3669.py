'''_3669.py

SpiralBevelGearSetCompoundSingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2003
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound import _3668, _3727, _3651
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _4318
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_SET_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses.Compound', 'SpiralBevelGearSetCompoundSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearSetCompoundSingleMeshWhineAnalysis',)


class SpiralBevelGearSetCompoundSingleMeshWhineAnalysis(_3651.BevelGearSetCompoundSingleMeshWhineAnalysis):
    '''SpiralBevelGearSetCompoundSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_SET_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearSetCompoundSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2003.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2003.SpiralBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2003.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2003.SpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def spiral_bevel_gears_compound_single_mesh_whine_analysis(self) -> 'List[_3668.SpiralBevelGearCompoundSingleMeshWhineAnalysis]':
        '''List[SpiralBevelGearCompoundSingleMeshWhineAnalysis]: 'SpiralBevelGearsCompoundSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearsCompoundSingleMeshWhineAnalysis, constructor.new(_3668.SpiralBevelGearCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def spiral_bevel_meshes_compound_single_mesh_whine_analysis(self) -> 'List[_3727.SpiralBevelGearMeshCompoundSingleMeshWhineAnalysis]':
        '''List[SpiralBevelGearMeshCompoundSingleMeshWhineAnalysis]: 'SpiralBevelMeshesCompoundSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelMeshesCompoundSingleMeshWhineAnalysis, constructor.new(_3727.SpiralBevelGearMeshCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_4318.SpiralBevelGearSetSingleMeshWhineAnalysis]':
        '''List[SpiralBevelGearSetSingleMeshWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4318.SpiralBevelGearSetSingleMeshWhineAnalysis))
        return value

    @property
    def assembly_single_mesh_whine_analysis_load_cases(self) -> 'List[_4318.SpiralBevelGearSetSingleMeshWhineAnalysis]':
        '''List[SpiralBevelGearSetSingleMeshWhineAnalysis]: 'AssemblySingleMeshWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySingleMeshWhineAnalysisLoadCases, constructor.new(_4318.SpiralBevelGearSetSingleMeshWhineAnalysis))
        return value
