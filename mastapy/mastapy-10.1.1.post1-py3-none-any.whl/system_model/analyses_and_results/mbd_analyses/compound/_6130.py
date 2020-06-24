'''_6130.py

RollingRingConnectionCompoundMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _1780
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses import _5999
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _6107
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_CONNECTION_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'RollingRingConnectionCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingConnectionCompoundMultiBodyDynamicsAnalysis',)


class RollingRingConnectionCompoundMultiBodyDynamicsAnalysis(_6107.InterMountableComponentConnectionCompoundMultiBodyDynamicsAnalysis):
    '''RollingRingConnectionCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_CONNECTION_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingConnectionCompoundMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1780.RollingRingConnection':
        '''RollingRingConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1780.RollingRingConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1780.RollingRingConnection':
        '''RollingRingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1780.RollingRingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5999.RollingRingConnectionMultiBodyDynamicsAnalysis]':
        '''List[RollingRingConnectionMultiBodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5999.RollingRingConnectionMultiBodyDynamicsAnalysis))
        return value

    @property
    def connection_multi_body_dynamics_analysis_load_cases(self) -> 'List[_5999.RollingRingConnectionMultiBodyDynamicsAnalysis]':
        '''List[RollingRingConnectionMultiBodyDynamicsAnalysis]: 'ConnectionMultiBodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionMultiBodyDynamicsAnalysisLoadCases, constructor.new(_5999.RollingRingConnectionMultiBodyDynamicsAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[RollingRingConnectionCompoundMultiBodyDynamicsAnalysis]':
        '''List[RollingRingConnectionCompoundMultiBodyDynamicsAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(RollingRingConnectionCompoundMultiBodyDynamicsAnalysis))
        return value
