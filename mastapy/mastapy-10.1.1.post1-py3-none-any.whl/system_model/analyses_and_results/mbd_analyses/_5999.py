'''_5999.py

RollingRingConnectionMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.connections_and_sockets import _1780
from mastapy.system_model.analyses_and_results.static_loads import _2222
from mastapy.system_model.analyses_and_results.mbd_analyses import _5973
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_CONNECTION_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'RollingRingConnectionMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingConnectionMultiBodyDynamicsAnalysis',)


class RollingRingConnectionMultiBodyDynamicsAnalysis(_5973.InterMountableComponentConnectionMultiBodyDynamicsAnalysis):
    '''RollingRingConnectionMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_CONNECTION_MULTI_BODY_DYNAMICS_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingConnectionMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def separation(self) -> 'float':
        '''float: 'Separation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Separation

    @property
    def normal_force(self) -> 'float':
        '''float: 'NormalForce' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NormalForce

    @property
    def connection_design(self) -> '_1780.RollingRingConnection':
        '''RollingRingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1780.RollingRingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_2222.RollingRingConnectionLoadCase':
        '''RollingRingConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2222.RollingRingConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def planetaries(self) -> 'List[RollingRingConnectionMultiBodyDynamicsAnalysis]':
        '''List[RollingRingConnectionMultiBodyDynamicsAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(RollingRingConnectionMultiBodyDynamicsAnalysis))
        return value
