'''_5692.py

FaceGearMeshModalAnalysisAtASpeed
'''


from mastapy.system_model.connections_and_sockets.gears import _1800
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2236
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _5696
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_MESH_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'FaceGearMeshModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearMeshModalAnalysisAtASpeed',)


class FaceGearMeshModalAnalysisAtASpeed(_5696.GearMeshModalAnalysisAtASpeed):
    '''FaceGearMeshModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_MESH_MODAL_ANALYSIS_AT_A_SPEED
    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearMeshModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1800.FaceGearMesh':
        '''FaceGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1800.FaceGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_2236.FaceGearMeshLoadCase':
        '''FaceGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2236.FaceGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
