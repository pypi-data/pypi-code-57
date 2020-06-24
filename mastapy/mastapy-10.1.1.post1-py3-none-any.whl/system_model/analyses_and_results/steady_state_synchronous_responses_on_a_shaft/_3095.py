'''_3095.py

SynchroniserSleeveSteadyStateSynchronousResponseOnAShaft
'''


from mastapy.system_model.part_model.couplings import _2034
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2204
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _3094
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_SLEEVE_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft', 'SynchroniserSleeveSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserSleeveSteadyStateSynchronousResponseOnAShaft',)


class SynchroniserSleeveSteadyStateSynchronousResponseOnAShaft(_3094.SynchroniserPartSteadyStateSynchronousResponseOnAShaft):
    '''SynchroniserSleeveSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_SLEEVE_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserSleeveSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2034.SynchroniserSleeve':
        '''SynchroniserSleeve: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2034.SynchroniserSleeve)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2204.SynchroniserSleeveLoadCase':
        '''SynchroniserSleeveLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2204.SynchroniserSleeveLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
