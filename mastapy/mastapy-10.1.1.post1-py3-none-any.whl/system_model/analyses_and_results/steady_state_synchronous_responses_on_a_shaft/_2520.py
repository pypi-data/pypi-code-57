'''_2520.py

CylindricalGearSetSteadyStateSynchronousResponseOnAShaft
'''


from typing import List

from mastapy.system_model.part_model.gears import _2065
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6095
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2521, _2519, _2530
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft', 'CylindricalGearSetSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetSteadyStateSynchronousResponseOnAShaft',)


class CylindricalGearSetSteadyStateSynchronousResponseOnAShaft(_2530.GearSetSteadyStateSynchronousResponseOnAShaft):
    '''CylindricalGearSetSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2065.CylindricalGearSet':
        '''CylindricalGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2065.CylindricalGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6095.CylindricalGearSetLoadCase':
        '''CylindricalGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6095.CylindricalGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def cylindrical_gears_steady_state_synchronous_response_on_a_shaft(self) -> 'List[_2521.CylindricalGearSteadyStateSynchronousResponseOnAShaft]':
        '''List[CylindricalGearSteadyStateSynchronousResponseOnAShaft]: 'CylindricalGearsSteadyStateSynchronousResponseOnAShaft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearsSteadyStateSynchronousResponseOnAShaft, constructor.new(_2521.CylindricalGearSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def cylindrical_meshes_steady_state_synchronous_response_on_a_shaft(self) -> 'List[_2519.CylindricalGearMeshSteadyStateSynchronousResponseOnAShaft]':
        '''List[CylindricalGearMeshSteadyStateSynchronousResponseOnAShaft]: 'CylindricalMeshesSteadyStateSynchronousResponseOnAShaft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshesSteadyStateSynchronousResponseOnAShaft, constructor.new(_2519.CylindricalGearMeshSteadyStateSynchronousResponseOnAShaft))
        return value
