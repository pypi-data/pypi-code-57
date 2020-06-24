'''_5358.py

RollingRingConnectionGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _1852
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6170
from mastapy.system_model.analyses_and_results.system_deflections import _2302
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5332
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_CONNECTION_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'RollingRingConnectionGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingConnectionGearWhineAnalysis',)


class RollingRingConnectionGearWhineAnalysis(_5332.InterMountableComponentConnectionGearWhineAnalysis):
    '''RollingRingConnectionGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_CONNECTION_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingConnectionGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1852.RollingRingConnection':
        '''RollingRingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1852.RollingRingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6170.RollingRingConnectionLoadCase':
        '''RollingRingConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6170.RollingRingConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def system_deflection_results(self) -> '_2302.RollingRingConnectionSystemDeflection':
        '''RollingRingConnectionSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2302.RollingRingConnectionSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def planetaries(self) -> 'List[RollingRingConnectionGearWhineAnalysis]':
        '''List[RollingRingConnectionGearWhineAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(RollingRingConnectionGearWhineAnalysis))
        return value
