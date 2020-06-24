'''_2835.py

UnbalancedMassSteadyStateSynchronousResponseAtASpeed
'''


from mastapy.system_model.part_model import _2018
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6207
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _2836
from mastapy._internal.python_net import python_net_import

_UNBALANCED_MASS_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed', 'UnbalancedMassSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('UnbalancedMassSteadyStateSynchronousResponseAtASpeed',)


class UnbalancedMassSteadyStateSynchronousResponseAtASpeed(_2836.VirtualComponentSteadyStateSynchronousResponseAtASpeed):
    '''UnbalancedMassSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _UNBALANCED_MASS_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'UnbalancedMassSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2018.UnbalancedMass':
        '''UnbalancedMass: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2018.UnbalancedMass)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6207.UnbalancedMassLoadCase':
        '''UnbalancedMassLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6207.UnbalancedMassLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
