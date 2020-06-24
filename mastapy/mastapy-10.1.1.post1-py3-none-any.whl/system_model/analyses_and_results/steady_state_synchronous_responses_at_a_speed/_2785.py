'''_2785.py

KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _2078
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6144
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _2786, _2784, _2782
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed', 'KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseAtASpeed',)


class KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseAtASpeed(_2782.KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponseAtASpeed):
    '''KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2078.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2078.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6144.KlingelnbergCycloPalloidHypoidGearSetLoadCase':
        '''KlingelnbergCycloPalloidHypoidGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6144.KlingelnbergCycloPalloidHypoidGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def klingelnberg_cyclo_palloid_hypoid_gears_steady_state_synchronous_response_at_a_speed(self) -> 'List[_2786.KlingelnbergCycloPalloidHypoidGearSteadyStateSynchronousResponseAtASpeed]':
        '''List[KlingelnbergCycloPalloidHypoidGearSteadyStateSynchronousResponseAtASpeed]: 'KlingelnbergCycloPalloidHypoidGearsSteadyStateSynchronousResponseAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearsSteadyStateSynchronousResponseAtASpeed, constructor.new(_2786.KlingelnbergCycloPalloidHypoidGearSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes_steady_state_synchronous_response_at_a_speed(self) -> 'List[_2784.KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponseAtASpeed]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponseAtASpeed]: 'KlingelnbergCycloPalloidHypoidMeshesSteadyStateSynchronousResponseAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidMeshesSteadyStateSynchronousResponseAtASpeed, constructor.new(_2784.KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponseAtASpeed))
        return value
