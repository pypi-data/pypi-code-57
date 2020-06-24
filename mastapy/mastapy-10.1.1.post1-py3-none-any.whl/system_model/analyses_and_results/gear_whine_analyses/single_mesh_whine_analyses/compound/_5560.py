'''_5560.py

ConceptGearSetCompoundSingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2061
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound import _5558, _5559, _5584
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5436
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses.Compound', 'ConceptGearSetCompoundSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetCompoundSingleMeshWhineAnalysis',)


class ConceptGearSetCompoundSingleMeshWhineAnalysis(_5584.GearSetCompoundSingleMeshWhineAnalysis):
    '''ConceptGearSetCompoundSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetCompoundSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2061.ConceptGearSet':
        '''ConceptGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2061.ConceptGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2061.ConceptGearSet':
        '''ConceptGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2061.ConceptGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def concept_gears_compound_single_mesh_whine_analysis(self) -> 'List[_5558.ConceptGearCompoundSingleMeshWhineAnalysis]':
        '''List[ConceptGearCompoundSingleMeshWhineAnalysis]: 'ConceptGearsCompoundSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearsCompoundSingleMeshWhineAnalysis, constructor.new(_5558.ConceptGearCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def concept_meshes_compound_single_mesh_whine_analysis(self) -> 'List[_5559.ConceptGearMeshCompoundSingleMeshWhineAnalysis]':
        '''List[ConceptGearMeshCompoundSingleMeshWhineAnalysis]: 'ConceptMeshesCompoundSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshesCompoundSingleMeshWhineAnalysis, constructor.new(_5559.ConceptGearMeshCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5436.ConceptGearSetSingleMeshWhineAnalysis]':
        '''List[ConceptGearSetSingleMeshWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5436.ConceptGearSetSingleMeshWhineAnalysis))
        return value

    @property
    def assembly_single_mesh_whine_analysis_load_cases(self) -> 'List[_5436.ConceptGearSetSingleMeshWhineAnalysis]':
        '''List[ConceptGearSetSingleMeshWhineAnalysis]: 'AssemblySingleMeshWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySingleMeshWhineAnalysisLoadCases, constructor.new(_5436.ConceptGearSetSingleMeshWhineAnalysis))
        return value
