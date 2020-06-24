'''_3188.py

StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model.gears import _2085
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import _3186, _3187, _3105
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3066
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound', 'StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponse',)


class StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponse(_3105.BevelGearSetCompoundSteadyStateSynchronousResponse):
    '''StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2085.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2085.StraightBevelDiffGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2085.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2085.StraightBevelDiffGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def straight_bevel_diff_gears_compound_steady_state_synchronous_response(self) -> 'List[_3186.StraightBevelDiffGearCompoundSteadyStateSynchronousResponse]':
        '''List[StraightBevelDiffGearCompoundSteadyStateSynchronousResponse]: 'StraightBevelDiffGearsCompoundSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearsCompoundSteadyStateSynchronousResponse, constructor.new(_3186.StraightBevelDiffGearCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def straight_bevel_diff_meshes_compound_steady_state_synchronous_response(self) -> 'List[_3187.StraightBevelDiffGearMeshCompoundSteadyStateSynchronousResponse]':
        '''List[StraightBevelDiffGearMeshCompoundSteadyStateSynchronousResponse]: 'StraightBevelDiffMeshesCompoundSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshesCompoundSteadyStateSynchronousResponse, constructor.new(_3187.StraightBevelDiffGearMeshCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_3066.StraightBevelDiffGearSetSteadyStateSynchronousResponse]':
        '''List[StraightBevelDiffGearSetSteadyStateSynchronousResponse]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3066.StraightBevelDiffGearSetSteadyStateSynchronousResponse))
        return value

    @property
    def assembly_steady_state_synchronous_response_load_cases(self) -> 'List[_3066.StraightBevelDiffGearSetSteadyStateSynchronousResponse]':
        '''List[StraightBevelDiffGearSetSteadyStateSynchronousResponse]: 'AssemblySteadyStateSynchronousResponseLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySteadyStateSynchronousResponseLoadCases, constructor.new(_3066.StraightBevelDiffGearSetSteadyStateSynchronousResponse))
        return value
