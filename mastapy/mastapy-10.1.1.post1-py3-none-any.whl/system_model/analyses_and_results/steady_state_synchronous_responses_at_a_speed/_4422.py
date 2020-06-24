'''_4422.py

BevelDifferentialGearMeshSteadyStateSynchronousResponseAtASpeed
'''


from mastapy.system_model.connections_and_sockets.gears import _1790
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2233
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _4427
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_MESH_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed', 'BevelDifferentialGearMeshSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearMeshSteadyStateSynchronousResponseAtASpeed',)


class BevelDifferentialGearMeshSteadyStateSynchronousResponseAtASpeed(_4427.BevelGearMeshSteadyStateSynchronousResponseAtASpeed):
    '''BevelDifferentialGearMeshSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_MESH_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearMeshSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1790.BevelDifferentialGearMesh':
        '''BevelDifferentialGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1790.BevelDifferentialGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_2233.BevelDifferentialGearMeshLoadCase':
        '''BevelDifferentialGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2233.BevelDifferentialGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
