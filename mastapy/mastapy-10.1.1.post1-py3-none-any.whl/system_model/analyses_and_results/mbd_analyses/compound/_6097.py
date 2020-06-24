'''_6097.py

FaceGearSetCompoundMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _1978
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _6095, _6096, _6101
from mastapy.system_model.analyses_and_results.mbd_analyses import _5958
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'FaceGearSetCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetCompoundMultiBodyDynamicsAnalysis',)


class FaceGearSetCompoundMultiBodyDynamicsAnalysis(_6101.GearSetCompoundMultiBodyDynamicsAnalysis):
    '''FaceGearSetCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetCompoundMultiBodyDynamicsAnalysis.TYPE'):
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
    def face_gears_compound_multi_body_dynamics_analysis(self) -> 'List[_6095.FaceGearCompoundMultiBodyDynamicsAnalysis]':
        '''List[FaceGearCompoundMultiBodyDynamicsAnalysis]: 'FaceGearsCompoundMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsCompoundMultiBodyDynamicsAnalysis, constructor.new(_6095.FaceGearCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def face_meshes_compound_multi_body_dynamics_analysis(self) -> 'List[_6096.FaceGearMeshCompoundMultiBodyDynamicsAnalysis]':
        '''List[FaceGearMeshCompoundMultiBodyDynamicsAnalysis]: 'FaceMeshesCompoundMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesCompoundMultiBodyDynamicsAnalysis, constructor.new(_6096.FaceGearMeshCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5958.FaceGearSetMultiBodyDynamicsAnalysis]':
        '''List[FaceGearSetMultiBodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5958.FaceGearSetMultiBodyDynamicsAnalysis))
        return value

    @property
    def assembly_multi_body_dynamics_analysis_load_cases(self) -> 'List[_5958.FaceGearSetMultiBodyDynamicsAnalysis]':
        '''List[FaceGearSetMultiBodyDynamicsAnalysis]: 'AssemblyMultiBodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyMultiBodyDynamicsAnalysisLoadCases, constructor.new(_5958.FaceGearSetMultiBodyDynamicsAnalysis))
        return value
