'''_4831.py

HypoidGearSetCompoundSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model.gears import _1965
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import _4829, _4830, _4778
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _4710
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound', 'HypoidGearSetCompoundSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSetCompoundSteadyStateSynchronousResponse',)


class HypoidGearSetCompoundSteadyStateSynchronousResponse(_4778.AGMAGleasonConicalGearSetCompoundSteadyStateSynchronousResponse):
    '''HypoidGearSetCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_SET_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearSetCompoundSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1965.HypoidGearSet':
        '''HypoidGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1965.HypoidGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1965.HypoidGearSet':
        '''HypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1965.HypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def hypoid_gears_compound_steady_state_synchronous_response(self) -> 'List[_4829.HypoidGearCompoundSteadyStateSynchronousResponse]':
        '''List[HypoidGearCompoundSteadyStateSynchronousResponse]: 'HypoidGearsCompoundSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearsCompoundSteadyStateSynchronousResponse, constructor.new(_4829.HypoidGearCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def hypoid_meshes_compound_steady_state_synchronous_response(self) -> 'List[_4830.HypoidGearMeshCompoundSteadyStateSynchronousResponse]':
        '''List[HypoidGearMeshCompoundSteadyStateSynchronousResponse]: 'HypoidMeshesCompoundSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidMeshesCompoundSteadyStateSynchronousResponse, constructor.new(_4830.HypoidGearMeshCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_4710.HypoidGearSetSteadyStateSynchronousResponse]':
        '''List[HypoidGearSetSteadyStateSynchronousResponse]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4710.HypoidGearSetSteadyStateSynchronousResponse))
        return value

    @property
    def assembly_steady_state_synchronous_response_load_cases(self) -> 'List[_4710.HypoidGearSetSteadyStateSynchronousResponse]':
        '''List[HypoidGearSetSteadyStateSynchronousResponse]: 'AssemblySteadyStateSynchronousResponseLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySteadyStateSynchronousResponseLoadCases, constructor.new(_4710.HypoidGearSetSteadyStateSynchronousResponse))
        return value
