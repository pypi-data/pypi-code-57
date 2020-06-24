'''_4385.py

SpiralBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft
'''


from typing import List

from mastapy.system_model.part_model.gears import _1988
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import _4383, _4384, _3125
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _3079
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_SET_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft.Compound', 'SpiralBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft',)


class SpiralBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft(_3125.BevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft):
    '''SpiralBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_SET_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1988.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1988.SpiralBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1988.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1988.SpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def spiral_bevel_gears_compound_steady_state_synchronous_response_on_a_shaft(self) -> 'List[_4383.SpiralBevelGearCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[SpiralBevelGearCompoundSteadyStateSynchronousResponseOnAShaft]: 'SpiralBevelGearsCompoundSteadyStateSynchronousResponseOnAShaft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearsCompoundSteadyStateSynchronousResponseOnAShaft, constructor.new(_4383.SpiralBevelGearCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def spiral_bevel_meshes_compound_steady_state_synchronous_response_on_a_shaft(self) -> 'List[_4384.SpiralBevelGearMeshCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[SpiralBevelGearMeshCompoundSteadyStateSynchronousResponseOnAShaft]: 'SpiralBevelMeshesCompoundSteadyStateSynchronousResponseOnAShaft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelMeshesCompoundSteadyStateSynchronousResponseOnAShaft, constructor.new(_4384.SpiralBevelGearMeshCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_3079.SpiralBevelGearSetSteadyStateSynchronousResponseOnAShaft]':
        '''List[SpiralBevelGearSetSteadyStateSynchronousResponseOnAShaft]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3079.SpiralBevelGearSetSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def assembly_steady_state_synchronous_response_on_a_shaft_load_cases(self) -> 'List[_3079.SpiralBevelGearSetSteadyStateSynchronousResponseOnAShaft]':
        '''List[SpiralBevelGearSetSteadyStateSynchronousResponseOnAShaft]: 'AssemblySteadyStateSynchronousResponseOnAShaftLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySteadyStateSynchronousResponseOnAShaftLoadCases, constructor.new(_3079.SpiralBevelGearSetSteadyStateSynchronousResponseOnAShaft))
        return value
