'''_2578.py

StraightBevelDiffGearSteadyStateSynchronousResponseOnAShaft
'''


from mastapy.system_model.part_model.gears import _2084
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6185
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2494
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft', 'StraightBevelDiffGearSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSteadyStateSynchronousResponseOnAShaft',)


class StraightBevelDiffGearSteadyStateSynchronousResponseOnAShaft(_2494.BevelGearSteadyStateSynchronousResponseOnAShaft):
    '''StraightBevelDiffGearSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2084.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2084.StraightBevelDiffGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6185.StraightBevelDiffGearLoadCase':
        '''StraightBevelDiffGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6185.StraightBevelDiffGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
