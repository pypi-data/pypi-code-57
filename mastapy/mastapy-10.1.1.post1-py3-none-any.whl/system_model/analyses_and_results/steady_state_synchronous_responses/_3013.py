'''_3013.py

FaceGearSetSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model.gears import _2068
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6115
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3014, _3012, _3017
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'FaceGearSetSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetSteadyStateSynchronousResponse',)


class FaceGearSetSteadyStateSynchronousResponse(_3017.GearSetSteadyStateSynchronousResponse):
    '''FaceGearSetSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetSteadyStateSynchronousResponse.TYPE'):
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
    def face_gears_steady_state_synchronous_response(self) -> 'List[_3014.FaceGearSteadyStateSynchronousResponse]':
        '''List[FaceGearSteadyStateSynchronousResponse]: 'FaceGearsSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsSteadyStateSynchronousResponse, constructor.new(_3014.FaceGearSteadyStateSynchronousResponse))
        return value

    @property
    def face_meshes_steady_state_synchronous_response(self) -> 'List[_3012.FaceGearMeshSteadyStateSynchronousResponse]':
        '''List[FaceGearMeshSteadyStateSynchronousResponse]: 'FaceMeshesSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesSteadyStateSynchronousResponse, constructor.new(_3012.FaceGearMeshSteadyStateSynchronousResponse))
        return value
