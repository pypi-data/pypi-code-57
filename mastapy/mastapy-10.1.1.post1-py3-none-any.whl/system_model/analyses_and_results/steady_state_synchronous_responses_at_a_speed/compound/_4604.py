'''_4604.py

MassDiscCompoundSteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.part_model import _1926
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _4484
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import _4646
from mastapy._internal.python_net import python_net_import

_MASS_DISC_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound', 'MassDiscCompoundSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('MassDiscCompoundSteadyStateSynchronousResponseAtASpeed',)


class MassDiscCompoundSteadyStateSynchronousResponseAtASpeed(_4646.VirtualComponentCompoundSteadyStateSynchronousResponseAtASpeed):
    '''MassDiscCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _MASS_DISC_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED
    __hash__ = None

    def __init__(self, instance_to_wrap: 'MassDiscCompoundSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1926.MassDisc':
        '''MassDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1926.MassDisc)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4484.MassDiscSteadyStateSynchronousResponseAtASpeed]':
        '''List[MassDiscSteadyStateSynchronousResponseAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4484.MassDiscSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def component_steady_state_synchronous_response_at_a_speed_load_cases(self) -> 'List[_4484.MassDiscSteadyStateSynchronousResponseAtASpeed]':
        '''List[MassDiscSteadyStateSynchronousResponseAtASpeed]: 'ComponentSteadyStateSynchronousResponseAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSteadyStateSynchronousResponseAtASpeedLoadCases, constructor.new(_4484.MassDiscSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def planetaries(self) -> 'List[MassDiscCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[MassDiscCompoundSteadyStateSynchronousResponseAtASpeed]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(MassDiscCompoundSteadyStateSynchronousResponseAtASpeed))
        return value
