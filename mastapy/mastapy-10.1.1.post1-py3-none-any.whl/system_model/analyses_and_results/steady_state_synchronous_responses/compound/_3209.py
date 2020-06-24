'''_3209.py

ZerolBevelGearSetCompoundSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model.gears import _2093
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import _3207, _3208, _3105
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3087
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound', 'ZerolBevelGearSetCompoundSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetCompoundSteadyStateSynchronousResponse',)


class ZerolBevelGearSetCompoundSteadyStateSynchronousResponse(_3105.BevelGearSetCompoundSteadyStateSynchronousResponse):
    '''ZerolBevelGearSetCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetCompoundSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2093.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2093.ZerolBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2093.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2093.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def zerol_bevel_gears_compound_steady_state_synchronous_response(self) -> 'List[_3207.ZerolBevelGearCompoundSteadyStateSynchronousResponse]':
        '''List[ZerolBevelGearCompoundSteadyStateSynchronousResponse]: 'ZerolBevelGearsCompoundSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsCompoundSteadyStateSynchronousResponse, constructor.new(_3207.ZerolBevelGearCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def zerol_bevel_meshes_compound_steady_state_synchronous_response(self) -> 'List[_3208.ZerolBevelGearMeshCompoundSteadyStateSynchronousResponse]':
        '''List[ZerolBevelGearMeshCompoundSteadyStateSynchronousResponse]: 'ZerolBevelMeshesCompoundSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesCompoundSteadyStateSynchronousResponse, constructor.new(_3208.ZerolBevelGearMeshCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_3087.ZerolBevelGearSetSteadyStateSynchronousResponse]':
        '''List[ZerolBevelGearSetSteadyStateSynchronousResponse]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3087.ZerolBevelGearSetSteadyStateSynchronousResponse))
        return value

    @property
    def assembly_steady_state_synchronous_response_load_cases(self) -> 'List[_3087.ZerolBevelGearSetSteadyStateSynchronousResponse]':
        '''List[ZerolBevelGearSetSteadyStateSynchronousResponse]: 'AssemblySteadyStateSynchronousResponseLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySteadyStateSynchronousResponseLoadCases, constructor.new(_3087.ZerolBevelGearSetSteadyStateSynchronousResponse))
        return value
