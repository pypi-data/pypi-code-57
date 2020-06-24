'''_4611.py

PlanetCarrierCompoundSteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.part_model import _1932
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _4491
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import _4606
from mastapy._internal.python_net import python_net_import

_PLANET_CARRIER_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound', 'PlanetCarrierCompoundSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetCarrierCompoundSteadyStateSynchronousResponseAtASpeed',)


class PlanetCarrierCompoundSteadyStateSynchronousResponseAtASpeed(_4606.MountableComponentCompoundSteadyStateSynchronousResponseAtASpeed):
    '''PlanetCarrierCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _PLANET_CARRIER_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetCarrierCompoundSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1932.PlanetCarrier':
        '''PlanetCarrier: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1932.PlanetCarrier)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4491.PlanetCarrierSteadyStateSynchronousResponseAtASpeed]':
        '''List[PlanetCarrierSteadyStateSynchronousResponseAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4491.PlanetCarrierSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def component_steady_state_synchronous_response_at_a_speed_load_cases(self) -> 'List[_4491.PlanetCarrierSteadyStateSynchronousResponseAtASpeed]':
        '''List[PlanetCarrierSteadyStateSynchronousResponseAtASpeed]: 'ComponentSteadyStateSynchronousResponseAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSteadyStateSynchronousResponseAtASpeedLoadCases, constructor.new(_4491.PlanetCarrierSteadyStateSynchronousResponseAtASpeed))
        return value
