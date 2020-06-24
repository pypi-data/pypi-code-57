'''_2214.py

BeltConnectionSystemDeflection
'''


from mastapy._internal import constructor
from mastapy.system_model.connections_and_sockets import _1832
from mastapy.system_model.analyses_and_results.static_loads import _6055
from mastapy.system_model.analyses_and_results.power_flows import _3223
from mastapy.system_model.analyses_and_results.system_deflections import _2275
from mastapy._internal.python_net import python_net_import

_BELT_CONNECTION_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'BeltConnectionSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltConnectionSystemDeflection',)


class BeltConnectionSystemDeflection(_2275.InterMountableComponentConnectionSystemDeflection):
    '''BeltConnectionSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _BELT_CONNECTION_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltConnectionSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def extension(self) -> 'float':
        '''float: 'Extension' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Extension

    @property
    def extension_including_pre_tension(self) -> 'float':
        '''float: 'ExtensionIncludingPreTension' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ExtensionIncludingPreTension

    @property
    def force_in_loa(self) -> 'float':
        '''float: 'ForceInLOA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ForceInLOA

    @property
    def connection_design(self) -> '_1832.BeltConnection':
        '''BeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1832.BeltConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6055.BeltConnectionLoadCase':
        '''BeltConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6055.BeltConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def power_flow_results(self) -> '_3223.BeltConnectionPowerFlow':
        '''BeltConnectionPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3223.BeltConnectionPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None
