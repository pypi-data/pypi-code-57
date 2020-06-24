'''_4627.py

FaceGearSetCompoundModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _2068
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _4625, _4626, _4631
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4505
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'FaceGearSetCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetCompoundModalAnalysisAtASpeed',)


class FaceGearSetCompoundModalAnalysisAtASpeed(_4631.GearSetCompoundModalAnalysisAtASpeed):
    '''FaceGearSetCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetCompoundModalAnalysisAtASpeed.TYPE'):
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
    def face_gears_compound_modal_analysis_at_a_speed(self) -> 'List[_4625.FaceGearCompoundModalAnalysisAtASpeed]':
        '''List[FaceGearCompoundModalAnalysisAtASpeed]: 'FaceGearsCompoundModalAnalysisAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsCompoundModalAnalysisAtASpeed, constructor.new(_4625.FaceGearCompoundModalAnalysisAtASpeed))
        return value

    @property
    def face_meshes_compound_modal_analysis_at_a_speed(self) -> 'List[_4626.FaceGearMeshCompoundModalAnalysisAtASpeed]':
        '''List[FaceGearMeshCompoundModalAnalysisAtASpeed]: 'FaceMeshesCompoundModalAnalysisAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesCompoundModalAnalysisAtASpeed, constructor.new(_4626.FaceGearMeshCompoundModalAnalysisAtASpeed))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_4505.FaceGearSetModalAnalysisAtASpeed]':
        '''List[FaceGearSetModalAnalysisAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4505.FaceGearSetModalAnalysisAtASpeed))
        return value

    @property
    def assembly_modal_analysis_at_a_speed_load_cases(self) -> 'List[_4505.FaceGearSetModalAnalysisAtASpeed]':
        '''List[FaceGearSetModalAnalysisAtASpeed]: 'AssemblyModalAnalysisAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysisAtASpeedLoadCases, constructor.new(_4505.FaceGearSetModalAnalysisAtASpeed))
        return value
