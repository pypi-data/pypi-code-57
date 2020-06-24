'''_4980.py

HypoidGearMeshModalAnalysesAtStiffnesses
'''


from mastapy.system_model.connections_and_sockets.gears import _1804
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2246
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _4926
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_MESH_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'HypoidGearMeshModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearMeshModalAnalysesAtStiffnesses',)


class HypoidGearMeshModalAnalysesAtStiffnesses(_4926.AGMAGleasonConicalGearMeshModalAnalysesAtStiffnesses):
    '''HypoidGearMeshModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_MESH_MODAL_ANALYSES_AT_STIFFNESSES
    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearMeshModalAnalysesAtStiffnesses.TYPE'):
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
