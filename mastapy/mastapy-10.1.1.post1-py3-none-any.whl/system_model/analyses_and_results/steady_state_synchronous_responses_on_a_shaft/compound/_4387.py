'''_4387.py

SpringDamperConnectionCompoundSteadyStateSynchronousResponseOnAShaft
'''


from typing import List

from mastapy.system_model.connections_and_sockets.couplings import _1828
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _3081
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import _4331
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft.Compound', 'SpringDamperConnectionCompoundSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperConnectionCompoundSteadyStateSynchronousResponseOnAShaft',)


class SpringDamperConnectionCompoundSteadyStateSynchronousResponseOnAShaft(_4331.CouplingConnectionCompoundSteadyStateSynchronousResponseOnAShaft):
    '''SpringDamperConnectionCompoundSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperConnectionCompoundSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1828.SpringDamperConnection':
        '''SpringDamperConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1828.SpringDamperConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1828.SpringDamperConnection':
        '''SpringDamperConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1828.SpringDamperConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3081.SpringDamperConnectionSteadyStateSynchronousResponseOnAShaft]':
        '''List[SpringDamperConnectionSteadyStateSynchronousResponseOnAShaft]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3081.SpringDamperConnectionSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def connection_steady_state_synchronous_response_on_a_shaft_load_cases(self) -> 'List[_3081.SpringDamperConnectionSteadyStateSynchronousResponseOnAShaft]':
        '''List[SpringDamperConnectionSteadyStateSynchronousResponseOnAShaft]: 'ConnectionSteadyStateSynchronousResponseOnAShaftLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSteadyStateSynchronousResponseOnAShaftLoadCases, constructor.new(_3081.SpringDamperConnectionSteadyStateSynchronousResponseOnAShaft))
        return value
