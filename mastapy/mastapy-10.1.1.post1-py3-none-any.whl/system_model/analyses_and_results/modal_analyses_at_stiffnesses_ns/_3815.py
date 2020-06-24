'''_3815.py

SpiralBevelGearMeshModalAnalysesAtStiffnesses
'''


from mastapy.system_model.connections_and_sockets.gears import _1884
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6179
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3735
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_MESH_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'SpiralBevelGearMeshModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearMeshModalAnalysesAtStiffnesses',)


class SpiralBevelGearMeshModalAnalysesAtStiffnesses(_3735.BevelGearMeshModalAnalysesAtStiffnesses):
    '''SpiralBevelGearMeshModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_MESH_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearMeshModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1884.SpiralBevelGearMesh':
        '''SpiralBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1884.SpiralBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6179.SpiralBevelGearMeshLoadCase':
        '''SpiralBevelGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6179.SpiralBevelGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
