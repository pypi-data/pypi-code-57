'''_2769.py

FaceGearSetSteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _2068
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6115
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _2770, _2768, _2773
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed', 'FaceGearSetSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetSteadyStateSynchronousResponseAtASpeed',)


class FaceGearSetSteadyStateSynchronousResponseAtASpeed(_2773.GearSetSteadyStateSynchronousResponseAtASpeed):
    '''FaceGearSetSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2068.FaceGearSet':
        '''FaceGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2068.FaceGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6115.FaceGearSetLoadCase':
        '''FaceGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6115.FaceGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def face_gears_steady_state_synchronous_response_at_a_speed(self) -> 'List[_2770.FaceGearSteadyStateSynchronousResponseAtASpeed]':
        '''List[FaceGearSteadyStateSynchronousResponseAtASpeed]: 'FaceGearsSteadyStateSynchronousResponseAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsSteadyStateSynchronousResponseAtASpeed, constructor.new(_2770.FaceGearSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def face_meshes_steady_state_synchronous_response_at_a_speed(self) -> 'List[_2768.FaceGearMeshSteadyStateSynchronousResponseAtASpeed]':
        '''List[FaceGearMeshSteadyStateSynchronousResponseAtASpeed]: 'FaceMeshesSteadyStateSynchronousResponseAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesSteadyStateSynchronousResponseAtASpeed, constructor.new(_2768.FaceGearMeshSteadyStateSynchronousResponseAtASpeed))
        return value
