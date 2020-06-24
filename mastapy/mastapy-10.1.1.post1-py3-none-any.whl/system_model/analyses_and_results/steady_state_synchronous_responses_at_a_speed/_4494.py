'''_4494.py

PulleySteadyStateSynchronousResponseAtASpeed
'''


from mastapy.system_model.part_model.couplings import _2017
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2186
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _4449
from mastapy._internal.python_net import python_net_import

_PULLEY_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed', 'PulleySteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('PulleySteadyStateSynchronousResponseAtASpeed',)


class PulleySteadyStateSynchronousResponseAtASpeed(_4449.CouplingHalfSteadyStateSynchronousResponseAtASpeed):
    '''PulleySteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _PULLEY_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PulleySteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2017.Pulley':
        '''Pulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2017.Pulley)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2186.PulleyLoadCase':
        '''PulleyLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2186.PulleyLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
