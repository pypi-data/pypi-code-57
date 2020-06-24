'''_2831.py

PulleySteadyStateSynchronousResponseOnAShaft
'''


from mastapy.system_model.part_model.couplings import _2017
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2186
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2788
from mastapy._internal.python_net import python_net_import

_PULLEY_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft', 'PulleySteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('PulleySteadyStateSynchronousResponseOnAShaft',)


class PulleySteadyStateSynchronousResponseOnAShaft(_2788.CouplingHalfSteadyStateSynchronousResponseOnAShaft):
    '''PulleySteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _PULLEY_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PulleySteadyStateSynchronousResponseOnAShaft.TYPE'):
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
