'''_4419.py

BearingSteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.part_model import _1908
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2265
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _4447
from mastapy._internal.python_net import python_net_import

_BEARING_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed', 'BearingSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingSteadyStateSynchronousResponseAtASpeed',)


class BearingSteadyStateSynchronousResponseAtASpeed(_4447.ConnectorSteadyStateSynchronousResponseAtASpeed):
    '''BearingSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _BEARING_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1908.Bearing':
        '''Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1908.Bearing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2265.BearingLoadCase':
        '''BearingLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2265.BearingLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def planetaries(self) -> 'List[BearingSteadyStateSynchronousResponseAtASpeed]':
        '''List[BearingSteadyStateSynchronousResponseAtASpeed]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(BearingSteadyStateSynchronousResponseAtASpeed))
        return value
