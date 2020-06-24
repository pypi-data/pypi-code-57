'''_2934.py

KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponseOnAShaft
'''


from mastapy.system_model.connections_and_sockets.gears import _1808
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2250
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2931
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft', 'KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponseOnAShaft',)


class KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponseOnAShaft(_2931.KlingelnbergCycloPalloidConicalGearMeshSteadyStateSynchronousResponseOnAShaft):
    '''KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT
    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1808.KlingelnbergCycloPalloidHypoidGearMesh':
        '''KlingelnbergCycloPalloidHypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1808.KlingelnbergCycloPalloidHypoidGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_2250.KlingelnbergCycloPalloidHypoidGearMeshLoadCase':
        '''KlingelnbergCycloPalloidHypoidGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2250.KlingelnbergCycloPalloidHypoidGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
