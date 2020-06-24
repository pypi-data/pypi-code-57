'''_3286.py

FaceGearSetCompoundSingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _1978
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound import _3285, _3360, _3301
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _4363
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses.Compound', 'FaceGearSetCompoundSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetCompoundSingleMeshWhineAnalysis',)


class FaceGearSetCompoundSingleMeshWhineAnalysis(_3301.GearSetCompoundSingleMeshWhineAnalysis):
    '''FaceGearSetCompoundSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetCompoundSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1978.FaceGearSet':
        '''FaceGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1978.FaceGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1978.FaceGearSet':
        '''FaceGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1978.FaceGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def face_gears_compound_single_mesh_whine_analysis(self) -> 'List[_3285.FaceGearCompoundSingleMeshWhineAnalysis]':
        '''List[FaceGearCompoundSingleMeshWhineAnalysis]: 'FaceGearsCompoundSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsCompoundSingleMeshWhineAnalysis, constructor.new(_3285.FaceGearCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def face_meshes_compound_single_mesh_whine_analysis(self) -> 'List[_3360.FaceGearMeshCompoundSingleMeshWhineAnalysis]':
        '''List[FaceGearMeshCompoundSingleMeshWhineAnalysis]: 'FaceMeshesCompoundSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesCompoundSingleMeshWhineAnalysis, constructor.new(_3360.FaceGearMeshCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_4363.FaceGearSetSingleMeshWhineAnalysis]':
        '''List[FaceGearSetSingleMeshWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4363.FaceGearSetSingleMeshWhineAnalysis))
        return value

    @property
    def assembly_single_mesh_whine_analysis_load_cases(self) -> 'List[_4363.FaceGearSetSingleMeshWhineAnalysis]':
        '''List[FaceGearSetSingleMeshWhineAnalysis]: 'AssemblySingleMeshWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySingleMeshWhineAnalysisLoadCases, constructor.new(_4363.FaceGearSetSingleMeshWhineAnalysis))
        return value
