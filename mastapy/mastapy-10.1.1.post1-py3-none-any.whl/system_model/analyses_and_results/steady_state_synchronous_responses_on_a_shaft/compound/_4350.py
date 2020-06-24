'''_4350.py

HypoidGearCompoundSteadyStateSynchronousResponseOnAShaft
'''


from typing import List

from mastapy.system_model.part_model.gears import _2011
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2928
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import _3111
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft.Compound', 'HypoidGearCompoundSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearCompoundSteadyStateSynchronousResponseOnAShaft',)


class HypoidGearCompoundSteadyStateSynchronousResponseOnAShaft(_3111.AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseOnAShaft):
    '''HypoidGearCompoundSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT
    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearCompoundSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2011.HypoidGear':
        '''HypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2011.HypoidGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2928.HypoidGearSteadyStateSynchronousResponseOnAShaft]':
        '''List[HypoidGearSteadyStateSynchronousResponseOnAShaft]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2928.HypoidGearSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def component_steady_state_synchronous_response_on_a_shaft_load_cases(self) -> 'List[_2928.HypoidGearSteadyStateSynchronousResponseOnAShaft]':
        '''List[HypoidGearSteadyStateSynchronousResponseOnAShaft]: 'ComponentSteadyStateSynchronousResponseOnAShaftLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSteadyStateSynchronousResponseOnAShaftLoadCases, constructor.new(_2928.HypoidGearSteadyStateSynchronousResponseOnAShaft))
        return value
