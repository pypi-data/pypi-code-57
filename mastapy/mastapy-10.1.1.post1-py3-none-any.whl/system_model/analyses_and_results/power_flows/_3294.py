'''_3294.py

PlanetaryConnectionPowerFlow
'''


from mastapy.system_model.connections_and_sockets import _1848
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6159
from mastapy.system_model.analyses_and_results.power_flows import _3308
from mastapy._internal.python_net import python_net_import

_PLANETARY_CONNECTION_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'PlanetaryConnectionPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryConnectionPowerFlow',)


class PlanetaryConnectionPowerFlow(_3308.ShaftToMountableComponentConnectionPowerFlow):
    '''PlanetaryConnectionPowerFlow

    This is a mastapy class.
    '''

    TYPE = _PLANETARY_CONNECTION_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetaryConnectionPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1848.PlanetaryConnection':
        '''PlanetaryConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1848.PlanetaryConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6159.PlanetaryConnectionLoadCase':
        '''PlanetaryConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6159.PlanetaryConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
