'''_4170.py

StraightBevelGearMeshPowerFlow
'''


from mastapy.system_model.connections_and_sockets.gears import _1816
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2256
from mastapy.gears.rating.straight_bevel import _413
from mastapy.system_model.analyses_and_results.power_flows import _4161
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_MESH_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'StraightBevelGearMeshPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearMeshPowerFlow',)


class StraightBevelGearMeshPowerFlow(_4161.BevelGearMeshPowerFlow):
    '''StraightBevelGearMeshPowerFlow

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_MESH_POWER_FLOW
    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearMeshPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1816.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1816.StraightBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_2256.StraightBevelGearMeshLoadCase':
        '''StraightBevelGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2256.StraightBevelGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def rating(self) -> '_413.StraightBevelGearMeshRating':
        '''StraightBevelGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_413.StraightBevelGearMeshRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_413.StraightBevelGearMeshRating':
        '''StraightBevelGearMeshRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_413.StraightBevelGearMeshRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None
