'''_4515.py

StraightBevelGearSetSteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _1964
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2363
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _4516, _4514, _4428
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed', 'StraightBevelGearSetSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearSetSteadyStateSynchronousResponseAtASpeed',)


class StraightBevelGearSetSteadyStateSynchronousResponseAtASpeed(_4428.BevelGearSetSteadyStateSynchronousResponseAtASpeed):
    '''StraightBevelGearSetSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED
    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearSetSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1964.StraightBevelGearSet':
        '''StraightBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1964.StraightBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2363.StraightBevelGearSetLoadCase':
        '''StraightBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2363.StraightBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def straight_bevel_gears_steady_state_synchronous_response_at_a_speed(self) -> 'List[_4516.StraightBevelGearSteadyStateSynchronousResponseAtASpeed]':
        '''List[StraightBevelGearSteadyStateSynchronousResponseAtASpeed]: 'StraightBevelGearsSteadyStateSynchronousResponseAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearsSteadyStateSynchronousResponseAtASpeed, constructor.new(_4516.StraightBevelGearSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def straight_bevel_meshes_steady_state_synchronous_response_at_a_speed(self) -> 'List[_4514.StraightBevelGearMeshSteadyStateSynchronousResponseAtASpeed]':
        '''List[StraightBevelGearMeshSteadyStateSynchronousResponseAtASpeed]: 'StraightBevelMeshesSteadyStateSynchronousResponseAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelMeshesSteadyStateSynchronousResponseAtASpeed, constructor.new(_4514.StraightBevelGearMeshSteadyStateSynchronousResponseAtASpeed))
        return value
