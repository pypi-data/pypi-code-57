'''_2918.py

FaceGearMeshSteadyStateSynchronousResponseOnAShaft
'''


from mastapy.system_model.connections_and_sockets.gears import _1800
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2236
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2922
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_MESH_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft', 'FaceGearMeshSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearMeshSteadyStateSynchronousResponseOnAShaft',)


class FaceGearMeshSteadyStateSynchronousResponseOnAShaft(_2922.GearMeshSteadyStateSynchronousResponseOnAShaft):
    '''FaceGearMeshSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_MESH_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT
    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearMeshSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1800.FaceGearMesh':
        '''FaceGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1800.FaceGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_2236.FaceGearMeshLoadCase':
        '''FaceGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2236.FaceGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
