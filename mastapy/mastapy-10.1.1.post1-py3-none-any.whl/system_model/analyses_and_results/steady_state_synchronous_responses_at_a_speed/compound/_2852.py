'''_2852.py

BevelDifferentialGearCompoundSteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _2054
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _2732
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import _2857
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound', 'BevelDifferentialGearCompoundSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearCompoundSteadyStateSynchronousResponseAtASpeed',)


class BevelDifferentialGearCompoundSteadyStateSynchronousResponseAtASpeed(_2857.BevelGearCompoundSteadyStateSynchronousResponseAtASpeed):
    '''BevelDifferentialGearCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearCompoundSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2054.BevelDifferentialGear':
        '''BevelDifferentialGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2054.BevelDifferentialGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2732.BevelDifferentialGearSteadyStateSynchronousResponseAtASpeed]':
        '''List[BevelDifferentialGearSteadyStateSynchronousResponseAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2732.BevelDifferentialGearSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def component_steady_state_synchronous_response_at_a_speed_load_cases(self) -> 'List[_2732.BevelDifferentialGearSteadyStateSynchronousResponseAtASpeed]':
        '''List[BevelDifferentialGearSteadyStateSynchronousResponseAtASpeed]: 'ComponentSteadyStateSynchronousResponseAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSteadyStateSynchronousResponseAtASpeedLoadCases, constructor.new(_2732.BevelDifferentialGearSteadyStateSynchronousResponseAtASpeed))
        return value
