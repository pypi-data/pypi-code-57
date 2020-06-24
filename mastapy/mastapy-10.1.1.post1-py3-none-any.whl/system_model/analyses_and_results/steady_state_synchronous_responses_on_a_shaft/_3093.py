'''_3093.py

SynchroniserHalfSteadyStateSynchronousResponseOnAShaft
'''


from mastapy.system_model.part_model.couplings import _2033
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2200
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _3094
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_HALF_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft', 'SynchroniserHalfSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserHalfSteadyStateSynchronousResponseOnAShaft',)


class SynchroniserHalfSteadyStateSynchronousResponseOnAShaft(_3094.SynchroniserPartSteadyStateSynchronousResponseOnAShaft):
    '''SynchroniserHalfSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_HALF_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserHalfSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2033.SynchroniserHalf':
        '''SynchroniserHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2033.SynchroniserHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2200.SynchroniserHalfLoadCase':
        '''SynchroniserHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2200.SynchroniserHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
