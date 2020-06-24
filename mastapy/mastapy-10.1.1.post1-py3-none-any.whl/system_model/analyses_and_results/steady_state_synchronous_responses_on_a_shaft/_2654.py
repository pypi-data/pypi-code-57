'''_2654.py

ClutchHalfSteadyStateSynchronousResponseOnAShaft
'''


from mastapy.system_model.part_model.couplings import _2015
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2174
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2788
from mastapy._internal.python_net import python_net_import

_CLUTCH_HALF_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft', 'ClutchHalfSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchHalfSteadyStateSynchronousResponseOnAShaft',)


class ClutchHalfSteadyStateSynchronousResponseOnAShaft(_2788.CouplingHalfSteadyStateSynchronousResponseOnAShaft):
    '''ClutchHalfSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_HALF_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchHalfSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2015.ClutchHalf':
        '''ClutchHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2015.ClutchHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2174.ClutchHalfLoadCase':
        '''ClutchHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2174.ClutchHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
