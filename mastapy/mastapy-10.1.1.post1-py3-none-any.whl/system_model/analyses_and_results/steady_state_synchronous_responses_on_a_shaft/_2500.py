'''_2500.py

CoaxialConnectionSteadyStateSynchronousResponseOnAShaft
'''


from mastapy.system_model.connections_and_sockets import _1833
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6070
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2567
from mastapy._internal.python_net import python_net_import

_COAXIAL_CONNECTION_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft', 'CoaxialConnectionSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('CoaxialConnectionSteadyStateSynchronousResponseOnAShaft',)


class CoaxialConnectionSteadyStateSynchronousResponseOnAShaft(_2567.ShaftToMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft):
    '''CoaxialConnectionSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _COAXIAL_CONNECTION_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CoaxialConnectionSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1833.CoaxialConnection':
        '''CoaxialConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1833.CoaxialConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6070.CoaxialConnectionLoadCase':
        '''CoaxialConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6070.CoaxialConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
