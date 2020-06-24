'''_5497.py

SpiralBevelGearMeshModalAnalysisAtAStiffness
'''


from mastapy.system_model.connections_and_sockets.gears import _1812
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2254
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _5421
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_MESH_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'SpiralBevelGearMeshModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearMeshModalAnalysisAtAStiffness',)


class SpiralBevelGearMeshModalAnalysisAtAStiffness(_5421.BevelGearMeshModalAnalysisAtAStiffness):
    '''SpiralBevelGearMeshModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_MESH_MODAL_ANALYSIS_AT_A_STIFFNESS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearMeshModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1812.SpiralBevelGearMesh':
        '''SpiralBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1812.SpiralBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_2254.SpiralBevelGearMeshLoadCase':
        '''SpiralBevelGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2254.SpiralBevelGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
