'''_4376.py

RollingRingCompoundSteadyStateSynchronousResponseOnAShaft
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2027
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2953
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import _4332
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft.Compound', 'RollingRingCompoundSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingCompoundSteadyStateSynchronousResponseOnAShaft',)


class RollingRingCompoundSteadyStateSynchronousResponseOnAShaft(_4332.CouplingHalfCompoundSteadyStateSynchronousResponseOnAShaft):
    '''RollingRingCompoundSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT
    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingCompoundSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2027.RollingRing':
        '''RollingRing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2027.RollingRing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2953.RollingRingSteadyStateSynchronousResponseOnAShaft]':
        '''List[RollingRingSteadyStateSynchronousResponseOnAShaft]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2953.RollingRingSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def component_steady_state_synchronous_response_on_a_shaft_load_cases(self) -> 'List[_2953.RollingRingSteadyStateSynchronousResponseOnAShaft]':
        '''List[RollingRingSteadyStateSynchronousResponseOnAShaft]: 'ComponentSteadyStateSynchronousResponseOnAShaftLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSteadyStateSynchronousResponseOnAShaftLoadCases, constructor.new(_2953.RollingRingSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def planetaries(self) -> 'List[RollingRingCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[RollingRingCompoundSteadyStateSynchronousResponseOnAShaft]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(RollingRingCompoundSteadyStateSynchronousResponseOnAShaft))
        return value
