'''_2989.py

ZerolBevelGearSetSteadyStateSynchronousResponseOnAShaft
'''


from typing import List

from mastapy.system_model.part_model.gears import _1983
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2171
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2990, _2988, _2649
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft', 'ZerolBevelGearSetSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetSteadyStateSynchronousResponseOnAShaft',)


class ZerolBevelGearSetSteadyStateSynchronousResponseOnAShaft(_2649.BevelGearSetSteadyStateSynchronousResponseOnAShaft):
    '''ZerolBevelGearSetSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1983.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1983.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2171.ZerolBevelGearSetLoadCase':
        '''ZerolBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2171.ZerolBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def zerol_bevel_gears_steady_state_synchronous_response_on_a_shaft(self) -> 'List[_2990.ZerolBevelGearSteadyStateSynchronousResponseOnAShaft]':
        '''List[ZerolBevelGearSteadyStateSynchronousResponseOnAShaft]: 'ZerolBevelGearsSteadyStateSynchronousResponseOnAShaft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsSteadyStateSynchronousResponseOnAShaft, constructor.new(_2990.ZerolBevelGearSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def zerol_bevel_meshes_steady_state_synchronous_response_on_a_shaft(self) -> 'List[_2988.ZerolBevelGearMeshSteadyStateSynchronousResponseOnAShaft]':
        '''List[ZerolBevelGearMeshSteadyStateSynchronousResponseOnAShaft]: 'ZerolBevelMeshesSteadyStateSynchronousResponseOnAShaft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesSteadyStateSynchronousResponseOnAShaft, constructor.new(_2988.ZerolBevelGearMeshSteadyStateSynchronousResponseOnAShaft))
        return value
