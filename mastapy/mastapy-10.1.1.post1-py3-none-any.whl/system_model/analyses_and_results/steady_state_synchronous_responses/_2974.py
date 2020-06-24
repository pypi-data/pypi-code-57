'''_2974.py

BevelDifferentialGearSetSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model.gears import _2055
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6059
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _2975, _2973, _2979
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'BevelDifferentialGearSetSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSetSteadyStateSynchronousResponse',)


class BevelDifferentialGearSetSteadyStateSynchronousResponse(_2979.BevelGearSetSteadyStateSynchronousResponse):
    '''BevelDifferentialGearSetSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSetSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2055.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2055.BevelDifferentialGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6059.BevelDifferentialGearSetLoadCase':
        '''BevelDifferentialGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6059.BevelDifferentialGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def bevel_differential_gears_steady_state_synchronous_response(self) -> 'List[_2975.BevelDifferentialGearSteadyStateSynchronousResponse]':
        '''List[BevelDifferentialGearSteadyStateSynchronousResponse]: 'BevelDifferentialGearsSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearsSteadyStateSynchronousResponse, constructor.new(_2975.BevelDifferentialGearSteadyStateSynchronousResponse))
        return value

    @property
    def bevel_differential_meshes_steady_state_synchronous_response(self) -> 'List[_2973.BevelDifferentialGearMeshSteadyStateSynchronousResponse]':
        '''List[BevelDifferentialGearMeshSteadyStateSynchronousResponse]: 'BevelDifferentialMeshesSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialMeshesSteadyStateSynchronousResponse, constructor.new(_2973.BevelDifferentialGearMeshSteadyStateSynchronousResponse))
        return value
