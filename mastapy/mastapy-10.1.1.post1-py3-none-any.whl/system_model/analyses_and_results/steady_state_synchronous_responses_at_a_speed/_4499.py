'''_4499.py

ShaftHubConnectionSteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.couplings import _1967
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2188
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _4447
from mastapy._internal.python_net import python_net_import

_SHAFT_HUB_CONNECTION_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed', 'ShaftHubConnectionSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftHubConnectionSteadyStateSynchronousResponseAtASpeed',)


class ShaftHubConnectionSteadyStateSynchronousResponseAtASpeed(_4447.ConnectorSteadyStateSynchronousResponseAtASpeed):
    '''ShaftHubConnectionSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _SHAFT_HUB_CONNECTION_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftHubConnectionSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1967.ShaftHubConnection':
        '''ShaftHubConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1967.ShaftHubConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2188.ShaftHubConnectionLoadCase':
        '''ShaftHubConnectionLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2188.ShaftHubConnectionLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def planetaries(self) -> 'List[ShaftHubConnectionSteadyStateSynchronousResponseAtASpeed]':
        '''List[ShaftHubConnectionSteadyStateSynchronousResponseAtASpeed]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftHubConnectionSteadyStateSynchronousResponseAtASpeed))
        return value
