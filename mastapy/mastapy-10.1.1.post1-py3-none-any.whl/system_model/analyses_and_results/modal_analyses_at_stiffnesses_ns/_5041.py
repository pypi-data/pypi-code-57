'''_5041.py

WormGearMeshModalAnalysesAtStiffnesses
'''


from mastapy.system_model.connections_and_sockets.gears import _1818
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2258
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _4976
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_MESH_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'WormGearMeshModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearMeshModalAnalysesAtStiffnesses',)


class WormGearMeshModalAnalysesAtStiffnesses(_4976.GearMeshModalAnalysesAtStiffnesses):
    '''WormGearMeshModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_MESH_MODAL_ANALYSES_AT_STIFFNESSES
    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearMeshModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1818.WormGearMesh':
        '''WormGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1818.WormGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_2258.WormGearMeshLoadCase':
        '''WormGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2258.WormGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
