'''_2740.py

ClutchConnectionSteadyStateSynchronousResponseAtASpeed
'''


from mastapy.system_model.connections_and_sockets.couplings import _1894
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6067
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _2756
from mastapy._internal.python_net import python_net_import

_CLUTCH_CONNECTION_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed', 'ClutchConnectionSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchConnectionSteadyStateSynchronousResponseAtASpeed',)


class ClutchConnectionSteadyStateSynchronousResponseAtASpeed(_2756.CouplingConnectionSteadyStateSynchronousResponseAtASpeed):
    '''ClutchConnectionSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_CONNECTION_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchConnectionSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1894.ClutchConnection':
        '''ClutchConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1894.ClutchConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6067.ClutchConnectionLoadCase':
        '''ClutchConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6067.ClutchConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
