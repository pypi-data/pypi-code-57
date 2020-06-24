'''_3054.py

RollingRingConnectionAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _1780
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2275
from mastapy.system_model.analyses_and_results.system_deflections import _2228
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _3052
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_CONNECTION_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'RollingRingConnectionAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingConnectionAdvancedSystemDeflection',)


class RollingRingConnectionAdvancedSystemDeflection(_3052.InterMountableComponentConnectionAdvancedSystemDeflection):
    '''RollingRingConnectionAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_CONNECTION_ADVANCED_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingConnectionAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1780.RollingRingConnection':
        '''RollingRingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1780.RollingRingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_2275.RollingRingConnectionLoadCase':
        '''RollingRingConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2275.RollingRingConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def planetaries(self) -> 'List[RollingRingConnectionAdvancedSystemDeflection]':
        '''List[RollingRingConnectionAdvancedSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(RollingRingConnectionAdvancedSystemDeflection))
        return value

    @property
    def connection_system_deflection_results(self) -> 'List[_2228.RollingRingConnectionSystemDeflection]':
        '''List[RollingRingConnectionSystemDeflection]: 'ConnectionSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSystemDeflectionResults, constructor.new(_2228.RollingRingConnectionSystemDeflection))
        return value
