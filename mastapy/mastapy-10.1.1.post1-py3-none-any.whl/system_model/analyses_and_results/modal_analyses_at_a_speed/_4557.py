'''_4557.py

StraightBevelGearMeshModalAnalysisAtASpeed
'''


from mastapy.system_model.connections_and_sockets.gears import _1888
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6189
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4470
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_MESH_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'StraightBevelGearMeshModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearMeshModalAnalysisAtASpeed',)


class StraightBevelGearMeshModalAnalysisAtASpeed(_4470.BevelGearMeshModalAnalysisAtASpeed):
    '''StraightBevelGearMeshModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_MESH_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearMeshModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1888.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1888.StraightBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6189.StraightBevelGearMeshLoadCase':
        '''StraightBevelGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6189.StraightBevelGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
