'''_4167.py

KlingelnbergCycloPalloidHypoidGearMeshPowerFlow
'''


from mastapy.system_model.connections_and_sockets.gears import _1808
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2250
from mastapy.gears.rating.klingelnberg_hypoid import _419
from mastapy.system_model.analyses_and_results.power_flows import _4166
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'KlingelnbergCycloPalloidHypoidGearMeshPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearMeshPowerFlow',)


class KlingelnbergCycloPalloidHypoidGearMeshPowerFlow(_4166.KlingelnbergCycloPalloidConicalGearMeshPowerFlow):
    '''KlingelnbergCycloPalloidHypoidGearMeshPowerFlow

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH_POWER_FLOW
    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearMeshPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1808.KlingelnbergCycloPalloidHypoidGearMesh':
        '''KlingelnbergCycloPalloidHypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1808.KlingelnbergCycloPalloidHypoidGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_2250.KlingelnbergCycloPalloidHypoidGearMeshLoadCase':
        '''KlingelnbergCycloPalloidHypoidGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2250.KlingelnbergCycloPalloidHypoidGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def rating(self) -> '_419.KlingelnbergCycloPalloidHypoidGearMeshRating':
        '''KlingelnbergCycloPalloidHypoidGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_419.KlingelnbergCycloPalloidHypoidGearMeshRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_419.KlingelnbergCycloPalloidHypoidGearMeshRating':
        '''KlingelnbergCycloPalloidHypoidGearMeshRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_419.KlingelnbergCycloPalloidHypoidGearMeshRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None
