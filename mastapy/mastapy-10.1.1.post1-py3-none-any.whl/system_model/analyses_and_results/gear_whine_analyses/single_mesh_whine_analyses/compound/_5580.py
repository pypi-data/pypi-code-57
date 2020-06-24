'''_5580.py

FaceGearSetCompoundSingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2068
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound import _5578, _5579, _5584
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5456
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses.Compound', 'FaceGearSetCompoundSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetCompoundSingleMeshWhineAnalysis',)


class FaceGearSetCompoundSingleMeshWhineAnalysis(_5584.GearSetCompoundSingleMeshWhineAnalysis):
    '''FaceGearSetCompoundSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetCompoundSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2068.FaceGearSet':
        '''FaceGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2068.FaceGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2068.FaceGearSet':
        '''FaceGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2068.FaceGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def face_gears_compound_single_mesh_whine_analysis(self) -> 'List[_5578.FaceGearCompoundSingleMeshWhineAnalysis]':
        '''List[FaceGearCompoundSingleMeshWhineAnalysis]: 'FaceGearsCompoundSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsCompoundSingleMeshWhineAnalysis, constructor.new(_5578.FaceGearCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def face_meshes_compound_single_mesh_whine_analysis(self) -> 'List[_5579.FaceGearMeshCompoundSingleMeshWhineAnalysis]':
        '''List[FaceGearMeshCompoundSingleMeshWhineAnalysis]: 'FaceMeshesCompoundSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesCompoundSingleMeshWhineAnalysis, constructor.new(_5579.FaceGearMeshCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5456.FaceGearSetSingleMeshWhineAnalysis]':
        '''List[FaceGearSetSingleMeshWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5456.FaceGearSetSingleMeshWhineAnalysis))
        return value

    @property
    def assembly_single_mesh_whine_analysis_load_cases(self) -> 'List[_5456.FaceGearSetSingleMeshWhineAnalysis]':
        '''List[FaceGearSetSingleMeshWhineAnalysis]: 'AssemblySingleMeshWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySingleMeshWhineAnalysisLoadCases, constructor.new(_5456.FaceGearSetSingleMeshWhineAnalysis))
        return value
