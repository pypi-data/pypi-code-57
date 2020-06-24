'''_5700.py

HypoidGearMeshModalAnalysisAtASpeed
'''


from mastapy.system_model.connections_and_sockets.gears import _1804
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2246
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _5647
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_MESH_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'HypoidGearMeshModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearMeshModalAnalysisAtASpeed',)


class HypoidGearMeshModalAnalysisAtASpeed(_5647.AGMAGleasonConicalGearMeshModalAnalysisAtASpeed):
    '''HypoidGearMeshModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_MESH_MODAL_ANALYSIS_AT_A_SPEED
    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearMeshModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1804.HypoidGearMesh':
        '''HypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1804.HypoidGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_2246.HypoidGearMeshLoadCase':
        '''HypoidGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2246.HypoidGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
