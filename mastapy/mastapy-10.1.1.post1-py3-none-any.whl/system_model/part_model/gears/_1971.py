'''_1971.py

KlingelnbergCycloPalloidConicalGearSet
'''


from mastapy.gears.gear_designs.klingelnberg_conical import _957
from mastapy._internal import constructor
from mastapy.gears.gear_designs.klingelnberg_spiral_bevel import _389
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.klingelnberg_hypoid import _390
from mastapy.system_model.part_model.gears import _1969
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidConicalGearSet')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidConicalGearSet',)


class KlingelnbergCycloPalloidConicalGearSet(_1969.ConicalGearSet):
    '''KlingelnbergCycloPalloidConicalGearSet

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET
    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidConicalGearSet.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def conical_gear_set_design(self) -> '_957.KlingelnbergConicalGearSetDesign':
        '''KlingelnbergConicalGearSetDesign: 'ConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_957.KlingelnbergConicalGearSetDesign)(self.wrapped.ConicalGearSetDesign) if self.wrapped.ConicalGearSetDesign else None

    @property
    def conical_gear_set_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_design(self) -> '_389.KlingelnbergCycloPalloidSpiralBevelGearSetDesign':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetDesign: 'ConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConicalGearSetDesign.__class__.__qualname__ != 'KlingelnbergCycloPalloidSpiralBevelGearSetDesign':
            raise CastException('Failed to cast conical_gear_set_design to KlingelnbergCycloPalloidSpiralBevelGearSetDesign. Expected: {}.'.format(self.wrapped.ConicalGearSetDesign.__class__.__qualname__))

        return constructor.new(_389.KlingelnbergCycloPalloidSpiralBevelGearSetDesign)(self.wrapped.ConicalGearSetDesign) if self.wrapped.ConicalGearSetDesign else None

    @property
    def conical_gear_set_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set_design(self) -> '_390.KlingelnbergCycloPalloidHypoidGearSetDesign':
        '''KlingelnbergCycloPalloidHypoidGearSetDesign: 'ConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConicalGearSetDesign.__class__.__qualname__ != 'KlingelnbergCycloPalloidHypoidGearSetDesign':
            raise CastException('Failed to cast conical_gear_set_design to KlingelnbergCycloPalloidHypoidGearSetDesign. Expected: {}.'.format(self.wrapped.ConicalGearSetDesign.__class__.__qualname__))

        return constructor.new(_390.KlingelnbergCycloPalloidHypoidGearSetDesign)(self.wrapped.ConicalGearSetDesign) if self.wrapped.ConicalGearSetDesign else None

    @property
    def klingelnberg_conical_gear_set_design(self) -> '_957.KlingelnbergConicalGearSetDesign':
        '''KlingelnbergConicalGearSetDesign: 'KlingelnbergConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_957.KlingelnbergConicalGearSetDesign)(self.wrapped.KlingelnbergConicalGearSetDesign) if self.wrapped.KlingelnbergConicalGearSetDesign else None

    @property
    def klingelnberg_conical_gear_set_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_design(self) -> '_389.KlingelnbergCycloPalloidSpiralBevelGearSetDesign':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetDesign: 'KlingelnbergConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.KlingelnbergConicalGearSetDesign.__class__.__qualname__ != 'KlingelnbergCycloPalloidSpiralBevelGearSetDesign':
            raise CastException('Failed to cast klingelnberg_conical_gear_set_design to KlingelnbergCycloPalloidSpiralBevelGearSetDesign. Expected: {}.'.format(self.wrapped.KlingelnbergConicalGearSetDesign.__class__.__qualname__))

        return constructor.new(_389.KlingelnbergCycloPalloidSpiralBevelGearSetDesign)(self.wrapped.KlingelnbergConicalGearSetDesign) if self.wrapped.KlingelnbergConicalGearSetDesign else None

    @property
    def klingelnberg_conical_gear_set_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set_design(self) -> '_390.KlingelnbergCycloPalloidHypoidGearSetDesign':
        '''KlingelnbergCycloPalloidHypoidGearSetDesign: 'KlingelnbergConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.KlingelnbergConicalGearSetDesign.__class__.__qualname__ != 'KlingelnbergCycloPalloidHypoidGearSetDesign':
            raise CastException('Failed to cast klingelnberg_conical_gear_set_design to KlingelnbergCycloPalloidHypoidGearSetDesign. Expected: {}.'.format(self.wrapped.KlingelnbergConicalGearSetDesign.__class__.__qualname__))

        return constructor.new(_390.KlingelnbergCycloPalloidHypoidGearSetDesign)(self.wrapped.KlingelnbergConicalGearSetDesign) if self.wrapped.KlingelnbergConicalGearSetDesign else None
