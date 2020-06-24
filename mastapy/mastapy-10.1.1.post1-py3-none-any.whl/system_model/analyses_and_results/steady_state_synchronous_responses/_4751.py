'''_4751.py

StraightBevelDiffGearSetSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model.gears import _1982
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2359
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _4752, _4750, _4668
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'StraightBevelDiffGearSetSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetSteadyStateSynchronousResponse',)


class StraightBevelDiffGearSetSteadyStateSynchronousResponse(_4668.BevelGearSetSteadyStateSynchronousResponse):
    '''StraightBevelDiffGearSetSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1982.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1982.StraightBevelDiffGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2359.StraightBevelDiffGearSetLoadCase':
        '''StraightBevelDiffGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2359.StraightBevelDiffGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def straight_bevel_diff_gears_steady_state_synchronous_response(self) -> 'List[_4752.StraightBevelDiffGearSteadyStateSynchronousResponse]':
        '''List[StraightBevelDiffGearSteadyStateSynchronousResponse]: 'StraightBevelDiffGearsSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearsSteadyStateSynchronousResponse, constructor.new(_4752.StraightBevelDiffGearSteadyStateSynchronousResponse))
        return value

    @property
    def straight_bevel_diff_meshes_steady_state_synchronous_response(self) -> 'List[_4750.StraightBevelDiffGearMeshSteadyStateSynchronousResponse]':
        '''List[StraightBevelDiffGearMeshSteadyStateSynchronousResponse]: 'StraightBevelDiffMeshesSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshesSteadyStateSynchronousResponse, constructor.new(_4750.StraightBevelDiffGearMeshSteadyStateSynchronousResponse))
        return value
