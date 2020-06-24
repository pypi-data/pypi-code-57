'''_4513.py

StraightBevelDiffGearSteadyStateSynchronousResponseAtASpeed
'''


from mastapy.system_model.part_model.gears import _2005
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2357
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _4429
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed', 'StraightBevelDiffGearSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSteadyStateSynchronousResponseAtASpeed',)


class StraightBevelDiffGearSteadyStateSynchronousResponseAtASpeed(_4429.BevelGearSteadyStateSynchronousResponseAtASpeed):
    '''StraightBevelDiffGearSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED
    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2005.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2005.StraightBevelDiffGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2357.StraightBevelDiffGearLoadCase':
        '''StraightBevelDiffGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2357.StraightBevelDiffGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
