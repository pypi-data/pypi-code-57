'''_2791.py

MeasurementComponentSteadyStateSynchronousResponseAtASpeed
'''


from mastapy.system_model.part_model import _2005
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6149
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _2836
from mastapy._internal.python_net import python_net_import

_MEASUREMENT_COMPONENT_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed', 'MeasurementComponentSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('MeasurementComponentSteadyStateSynchronousResponseAtASpeed',)


class MeasurementComponentSteadyStateSynchronousResponseAtASpeed(_2836.VirtualComponentSteadyStateSynchronousResponseAtASpeed):
    '''MeasurementComponentSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _MEASUREMENT_COMPONENT_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MeasurementComponentSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2005.MeasurementComponent':
        '''MeasurementComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2005.MeasurementComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6149.MeasurementComponentLoadCase':
        '''MeasurementComponentLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6149.MeasurementComponentLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
