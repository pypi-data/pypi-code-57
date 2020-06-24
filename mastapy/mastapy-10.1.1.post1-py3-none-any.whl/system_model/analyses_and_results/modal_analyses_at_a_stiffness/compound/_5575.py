'''_5575.py

FaceGearMeshCompoundModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1800
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _5455
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _5579
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_MESH_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'FaceGearMeshCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearMeshCompoundModalAnalysisAtAStiffness',)


class FaceGearMeshCompoundModalAnalysisAtAStiffness(_5579.GearMeshCompoundModalAnalysisAtAStiffness):
    '''FaceGearMeshCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_MESH_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearMeshCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1800.FaceGearMesh':
        '''FaceGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1800.FaceGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1800.FaceGearMesh':
        '''FaceGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1800.FaceGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5455.FaceGearMeshModalAnalysisAtAStiffness]':
        '''List[FaceGearMeshModalAnalysisAtAStiffness]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5455.FaceGearMeshModalAnalysisAtAStiffness))
        return value

    @property
    def connection_modal_analysis_at_a_stiffness_load_cases(self) -> 'List[_5455.FaceGearMeshModalAnalysisAtAStiffness]':
        '''List[FaceGearMeshModalAnalysisAtAStiffness]: 'ConnectionModalAnalysisAtAStiffnessLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionModalAnalysisAtAStiffnessLoadCases, constructor.new(_5455.FaceGearMeshModalAnalysisAtAStiffness))
        return value
