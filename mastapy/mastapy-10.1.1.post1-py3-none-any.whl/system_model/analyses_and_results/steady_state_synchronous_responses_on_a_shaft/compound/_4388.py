'''_4388.py

SpringDamperHalfCompoundSteadyStateSynchronousResponseOnAShaft
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2028
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _3082
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import _4332
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_HALF_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft.Compound', 'SpringDamperHalfCompoundSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperHalfCompoundSteadyStateSynchronousResponseOnAShaft',)


class SpringDamperHalfCompoundSteadyStateSynchronousResponseOnAShaft(_4332.CouplingHalfCompoundSteadyStateSynchronousResponseOnAShaft):
    '''SpringDamperHalfCompoundSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_HALF_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperHalfCompoundSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2028.SpringDamperHalf':
        '''SpringDamperHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2028.SpringDamperHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3082.SpringDamperHalfSteadyStateSynchronousResponseOnAShaft]':
        '''List[SpringDamperHalfSteadyStateSynchronousResponseOnAShaft]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3082.SpringDamperHalfSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def component_steady_state_synchronous_response_on_a_shaft_load_cases(self) -> 'List[_3082.SpringDamperHalfSteadyStateSynchronousResponseOnAShaft]':
        '''List[SpringDamperHalfSteadyStateSynchronousResponseOnAShaft]: 'ComponentSteadyStateSynchronousResponseOnAShaftLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSteadyStateSynchronousResponseOnAShaftLoadCases, constructor.new(_3082.SpringDamperHalfSteadyStateSynchronousResponseOnAShaft))
        return value
