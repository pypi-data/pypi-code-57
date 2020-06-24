'''_3338.py

ZerolBevelGearMeshPowerFlow
'''


from mastapy.system_model.connections_and_sockets.gears import _1892
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6213
from mastapy.gears.rating.zerol_bevel import _171
from mastapy.system_model.analyses_and_results.power_flows import _3230
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_MESH_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'ZerolBevelGearMeshPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearMeshPowerFlow',)


class ZerolBevelGearMeshPowerFlow(_3230.BevelGearMeshPowerFlow):
    '''ZerolBevelGearMeshPowerFlow

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_MESH_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearMeshPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1892.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1892.ZerolBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6213.ZerolBevelGearMeshLoadCase':
        '''ZerolBevelGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6213.ZerolBevelGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def rating(self) -> '_171.ZerolBevelGearMeshRating':
        '''ZerolBevelGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_171.ZerolBevelGearMeshRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_171.ZerolBevelGearMeshRating':
        '''ZerolBevelGearMeshRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_171.ZerolBevelGearMeshRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None
