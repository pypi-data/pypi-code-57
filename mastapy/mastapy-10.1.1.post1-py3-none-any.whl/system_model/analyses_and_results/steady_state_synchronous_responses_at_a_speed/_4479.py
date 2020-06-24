'''_4479.py

KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _1984
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2346
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _4480, _4478, _4476
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed', 'KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseAtASpeed',)


class KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseAtASpeed(_4476.KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponseAtASpeed):
    '''KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED
    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1984.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1984.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2346.KlingelnbergCycloPalloidHypoidGearSetLoadCase':
        '''KlingelnbergCycloPalloidHypoidGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2346.KlingelnbergCycloPalloidHypoidGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def klingelnberg_cyclo_palloid_hypoid_gears_steady_state_synchronous_response_at_a_speed(self) -> 'List[_4480.KlingelnbergCycloPalloidHypoidGearSteadyStateSynchronousResponseAtASpeed]':
        '''List[KlingelnbergCycloPalloidHypoidGearSteadyStateSynchronousResponseAtASpeed]: 'KlingelnbergCycloPalloidHypoidGearsSteadyStateSynchronousResponseAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearsSteadyStateSynchronousResponseAtASpeed, constructor.new(_4480.KlingelnbergCycloPalloidHypoidGearSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes_steady_state_synchronous_response_at_a_speed(self) -> 'List[_4478.KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponseAtASpeed]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponseAtASpeed]: 'KlingelnbergCycloPalloidHypoidMeshesSteadyStateSynchronousResponseAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidMeshesSteadyStateSynchronousResponseAtASpeed, constructor.new(_4478.KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponseAtASpeed))
        return value
