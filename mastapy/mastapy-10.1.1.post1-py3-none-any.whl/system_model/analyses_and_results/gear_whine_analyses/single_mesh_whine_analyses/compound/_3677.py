'''_3677.py

WormGearSetCompoundSingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2011
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound import _3676, _3729, _3658
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _4208
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses.Compound', 'WormGearSetCompoundSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetCompoundSingleMeshWhineAnalysis',)


class WormGearSetCompoundSingleMeshWhineAnalysis(_3658.GearSetCompoundSingleMeshWhineAnalysis):
    '''WormGearSetCompoundSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetCompoundSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2011.WormGearSet':
        '''WormGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2011.WormGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2011.WormGearSet':
        '''WormGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2011.WormGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def worm_gears_compound_single_mesh_whine_analysis(self) -> 'List[_3676.WormGearCompoundSingleMeshWhineAnalysis]':
        '''List[WormGearCompoundSingleMeshWhineAnalysis]: 'WormGearsCompoundSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearsCompoundSingleMeshWhineAnalysis, constructor.new(_3676.WormGearCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def worm_meshes_compound_single_mesh_whine_analysis(self) -> 'List[_3729.WormGearMeshCompoundSingleMeshWhineAnalysis]':
        '''List[WormGearMeshCompoundSingleMeshWhineAnalysis]: 'WormMeshesCompoundSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshesCompoundSingleMeshWhineAnalysis, constructor.new(_3729.WormGearMeshCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_4208.WormGearSetSingleMeshWhineAnalysis]':
        '''List[WormGearSetSingleMeshWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4208.WormGearSetSingleMeshWhineAnalysis))
        return value

    @property
    def assembly_single_mesh_whine_analysis_load_cases(self) -> 'List[_4208.WormGearSetSingleMeshWhineAnalysis]':
        '''List[WormGearSetSingleMeshWhineAnalysis]: 'AssemblySingleMeshWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySingleMeshWhineAnalysisLoadCases, constructor.new(_4208.WormGearSetSingleMeshWhineAnalysis))
        return value
