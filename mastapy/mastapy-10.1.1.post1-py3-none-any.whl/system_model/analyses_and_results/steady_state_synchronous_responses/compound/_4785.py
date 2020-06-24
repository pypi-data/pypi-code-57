'''_4785.py

BevelDifferentialGearSetCompoundSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model.gears import _1981
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import _4783, _4784, _4790
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _4663
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound', 'BevelDifferentialGearSetCompoundSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSetCompoundSteadyStateSynchronousResponse',)


class BevelDifferentialGearSetCompoundSteadyStateSynchronousResponse(_4790.BevelGearSetCompoundSteadyStateSynchronousResponse):
    '''BevelDifferentialGearSetCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSetCompoundSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1981.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1981.BevelDifferentialGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1981.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1981.BevelDifferentialGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def bevel_differential_gears_compound_steady_state_synchronous_response(self) -> 'List[_4783.BevelDifferentialGearCompoundSteadyStateSynchronousResponse]':
        '''List[BevelDifferentialGearCompoundSteadyStateSynchronousResponse]: 'BevelDifferentialGearsCompoundSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearsCompoundSteadyStateSynchronousResponse, constructor.new(_4783.BevelDifferentialGearCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def bevel_differential_meshes_compound_steady_state_synchronous_response(self) -> 'List[_4784.BevelDifferentialGearMeshCompoundSteadyStateSynchronousResponse]':
        '''List[BevelDifferentialGearMeshCompoundSteadyStateSynchronousResponse]: 'BevelDifferentialMeshesCompoundSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialMeshesCompoundSteadyStateSynchronousResponse, constructor.new(_4784.BevelDifferentialGearMeshCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_4663.BevelDifferentialGearSetSteadyStateSynchronousResponse]':
        '''List[BevelDifferentialGearSetSteadyStateSynchronousResponse]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4663.BevelDifferentialGearSetSteadyStateSynchronousResponse))
        return value

    @property
    def assembly_steady_state_synchronous_response_load_cases(self) -> 'List[_4663.BevelDifferentialGearSetSteadyStateSynchronousResponse]':
        '''List[BevelDifferentialGearSetSteadyStateSynchronousResponse]: 'AssemblySteadyStateSynchronousResponseLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySteadyStateSynchronousResponseLoadCases, constructor.new(_4663.BevelDifferentialGearSetSteadyStateSynchronousResponse))
        return value
