'''_4337.py

CylindricalGearMeshCompoundSteadyStateSynchronousResponseOnAShaft
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1798
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2912
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import _4347
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft.Compound', 'CylindricalGearMeshCompoundSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshCompoundSteadyStateSynchronousResponseOnAShaft',)


class CylindricalGearMeshCompoundSteadyStateSynchronousResponseOnAShaft(_4347.GearMeshCompoundSteadyStateSynchronousResponseOnAShaft):
    '''CylindricalGearMeshCompoundSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MESH_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshCompoundSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1798.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1798.CylindricalGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1798.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1798.CylindricalGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2912.CylindricalGearMeshSteadyStateSynchronousResponseOnAShaft]':
        '''List[CylindricalGearMeshSteadyStateSynchronousResponseOnAShaft]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2912.CylindricalGearMeshSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def connection_steady_state_synchronous_response_on_a_shaft_load_cases(self) -> 'List[_2912.CylindricalGearMeshSteadyStateSynchronousResponseOnAShaft]':
        '''List[CylindricalGearMeshSteadyStateSynchronousResponseOnAShaft]: 'ConnectionSteadyStateSynchronousResponseOnAShaftLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSteadyStateSynchronousResponseOnAShaftLoadCases, constructor.new(_2912.CylindricalGearMeshSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def planetaries(self) -> 'List[CylindricalGearMeshCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[CylindricalGearMeshCompoundSteadyStateSynchronousResponseOnAShaft]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(CylindricalGearMeshCompoundSteadyStateSynchronousResponseOnAShaft))
        return value
