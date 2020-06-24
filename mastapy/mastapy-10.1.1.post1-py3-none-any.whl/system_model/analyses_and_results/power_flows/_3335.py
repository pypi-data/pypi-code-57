'''_3335.py

WormGearMeshPowerFlow
'''


from mastapy.system_model.connections_and_sockets.gears import _1890
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6210
from mastapy.gears.rating.worm import _175
from mastapy.system_model.analyses_and_results.power_flows import _3268
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_MESH_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'WormGearMeshPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearMeshPowerFlow',)


class WormGearMeshPowerFlow(_3268.GearMeshPowerFlow):
    '''WormGearMeshPowerFlow

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_MESH_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearMeshPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1890.WormGearMesh':
        '''WormGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1890.WormGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6210.WormGearMeshLoadCase':
        '''WormGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6210.WormGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def rating(self) -> '_175.WormGearMeshRating':
        '''WormGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_175.WormGearMeshRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_175.WormGearMeshRating':
        '''WormGearMeshRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_175.WormGearMeshRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None
