'''_2841.py

ZerolBevelGearSetSteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _2093
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6214
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _2842, _2840, _2736
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed', 'ZerolBevelGearSetSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetSteadyStateSynchronousResponseAtASpeed',)


class ZerolBevelGearSetSteadyStateSynchronousResponseAtASpeed(_2736.BevelGearSetSteadyStateSynchronousResponseAtASpeed):
    '''ZerolBevelGearSetSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2093.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2093.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6214.ZerolBevelGearSetLoadCase':
        '''ZerolBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6214.ZerolBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def zerol_bevel_gears_steady_state_synchronous_response_at_a_speed(self) -> 'List[_2842.ZerolBevelGearSteadyStateSynchronousResponseAtASpeed]':
        '''List[ZerolBevelGearSteadyStateSynchronousResponseAtASpeed]: 'ZerolBevelGearsSteadyStateSynchronousResponseAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsSteadyStateSynchronousResponseAtASpeed, constructor.new(_2842.ZerolBevelGearSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def zerol_bevel_meshes_steady_state_synchronous_response_at_a_speed(self) -> 'List[_2840.ZerolBevelGearMeshSteadyStateSynchronousResponseAtASpeed]':
        '''List[ZerolBevelGearMeshSteadyStateSynchronousResponseAtASpeed]: 'ZerolBevelMeshesSteadyStateSynchronousResponseAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesSteadyStateSynchronousResponseAtASpeed, constructor.new(_2840.ZerolBevelGearMeshSteadyStateSynchronousResponseAtASpeed))
        return value
