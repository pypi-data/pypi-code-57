'''_4715.py

KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponse
'''


from mastapy.system_model.part_model.gears import _1971, _1984, _1985
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _4684
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponse',)


class KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponse(_4684.ConicalGearSetSteadyStateSynchronousResponse):
    '''KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1971.KlingelnbergCycloPalloidConicalGearSet':
        '''KlingelnbergCycloPalloidConicalGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1971.KlingelnbergCycloPalloidConicalGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set(self) -> '_1984.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.AssemblyDesign.__class__.__qualname__ != 'KlingelnbergCycloPalloidHypoidGearSet':
            raise CastException('Failed to cast assembly_design to KlingelnbergCycloPalloidHypoidGearSet. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new(_1984.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self) -> '_1985.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.AssemblyDesign.__class__.__qualname__ != 'KlingelnbergCycloPalloidSpiralBevelGearSet':
            raise CastException('Failed to cast assembly_design to KlingelnbergCycloPalloidSpiralBevelGearSet. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new(_1985.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None
