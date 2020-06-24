'''_340.py

GearSetDutyCycleRating
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs import _375
from mastapy.gears.gear_designs.worm import _384
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.face import _385
from mastapy.gears.gear_designs.cylindrical import _386, _388
from mastapy.gears.gear_designs.concept import _387
from mastapy.gears.gear_designs.klingelnberg_spiral_bevel import _389
from mastapy.gears.gear_designs.klingelnberg_hypoid import _390
from mastapy.gears.gear_designs.hypoid import _391
from mastapy.gears.gear_designs.zerol_bevel import _392
from mastapy.gears.gear_designs.straight_bevel_diff import _393
from mastapy.gears.gear_designs.straight_bevel import _394
from mastapy.gears.gear_designs.spiral_bevel import _395
from mastapy.gears.rating import _329, _343, _326
from mastapy._internal.python_net import python_net_import

_GEAR_SET_DUTY_CYCLE_RATING = python_net_import('SMT.MastaAPI.Gears.Rating', 'GearSetDutyCycleRating')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetDutyCycleRating',)


class GearSetDutyCycleRating(_326.AbstractGearSetRating):
    '''GearSetDutyCycleRating

    This is a mastapy class.
    '''

    TYPE = _GEAR_SET_DUTY_CYCLE_RATING
    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearSetDutyCycleRating.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.'''

        return self.wrapped.Name

    @name.setter
    def name(self, value: 'str'):
        self.wrapped.Name = str(value) if value else None

    @property
    def total_duty_cycle_gear_set_reliability(self) -> 'float':
        '''float: 'TotalDutyCycleGearSetReliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalDutyCycleGearSetReliability

    @property
    def duty_cycle_name(self) -> 'str':
        '''str: 'DutyCycleName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DutyCycleName

    @property
    def set_face_widths_for_specified_safety_factors(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'SetFaceWidthsForSpecifiedSafetyFactors' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SetFaceWidthsForSpecifiedSafetyFactors

    @property
    def gear_set_design(self) -> '_375.GearSetDesign':
        '''GearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_375.GearSetDesign)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign else None

    @property
    def gear_set_design_of_type_worm_gear_set_design(self) -> '_384.WormGearSetDesign':
        '''WormGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearSetDesign.__class__.__qualname__ != 'WormGearSetDesign':
            raise CastException('Failed to cast gear_set_design to WormGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new(_384.WormGearSetDesign)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign else None

    @property
    def gear_set_design_of_type_face_gear_set_design(self) -> '_385.FaceGearSetDesign':
        '''FaceGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearSetDesign.__class__.__qualname__ != 'FaceGearSetDesign':
            raise CastException('Failed to cast gear_set_design to FaceGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new(_385.FaceGearSetDesign)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign else None

    @property
    def gear_set_design_of_type_cylindrical_gear_set_design(self) -> '_386.CylindricalGearSetDesign':
        '''CylindricalGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearSetDesign.__class__.__qualname__ != 'CylindricalGearSetDesign':
            raise CastException('Failed to cast gear_set_design to CylindricalGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new(_386.CylindricalGearSetDesign)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign else None

    @property
    def gear_set_design_of_type_concept_gear_set_design(self) -> '_387.ConceptGearSetDesign':
        '''ConceptGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearSetDesign.__class__.__qualname__ != 'ConceptGearSetDesign':
            raise CastException('Failed to cast gear_set_design to ConceptGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new(_387.ConceptGearSetDesign)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign else None

    @property
    def gear_set_design_of_type_cylindrical_planetary_gear_set_design(self) -> '_388.CylindricalPlanetaryGearSetDesign':
        '''CylindricalPlanetaryGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearSetDesign.__class__.__qualname__ != 'CylindricalPlanetaryGearSetDesign':
            raise CastException('Failed to cast gear_set_design to CylindricalPlanetaryGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new(_388.CylindricalPlanetaryGearSetDesign)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign else None

    @property
    def gear_set_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_design(self) -> '_389.KlingelnbergCycloPalloidSpiralBevelGearSetDesign':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearSetDesign.__class__.__qualname__ != 'KlingelnbergCycloPalloidSpiralBevelGearSetDesign':
            raise CastException('Failed to cast gear_set_design to KlingelnbergCycloPalloidSpiralBevelGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new(_389.KlingelnbergCycloPalloidSpiralBevelGearSetDesign)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign else None

    @property
    def gear_set_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set_design(self) -> '_390.KlingelnbergCycloPalloidHypoidGearSetDesign':
        '''KlingelnbergCycloPalloidHypoidGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearSetDesign.__class__.__qualname__ != 'KlingelnbergCycloPalloidHypoidGearSetDesign':
            raise CastException('Failed to cast gear_set_design to KlingelnbergCycloPalloidHypoidGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new(_390.KlingelnbergCycloPalloidHypoidGearSetDesign)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign else None

    @property
    def gear_set_design_of_type_hypoid_gear_set_design(self) -> '_391.HypoidGearSetDesign':
        '''HypoidGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearSetDesign.__class__.__qualname__ != 'HypoidGearSetDesign':
            raise CastException('Failed to cast gear_set_design to HypoidGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new(_391.HypoidGearSetDesign)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign else None

    @property
    def gear_set_design_of_type_zerol_bevel_gear_set_design(self) -> '_392.ZerolBevelGearSetDesign':
        '''ZerolBevelGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearSetDesign.__class__.__qualname__ != 'ZerolBevelGearSetDesign':
            raise CastException('Failed to cast gear_set_design to ZerolBevelGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new(_392.ZerolBevelGearSetDesign)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign else None

    @property
    def gear_set_design_of_type_straight_bevel_diff_gear_set_design(self) -> '_393.StraightBevelDiffGearSetDesign':
        '''StraightBevelDiffGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearSetDesign.__class__.__qualname__ != 'StraightBevelDiffGearSetDesign':
            raise CastException('Failed to cast gear_set_design to StraightBevelDiffGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new(_393.StraightBevelDiffGearSetDesign)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign else None

    @property
    def gear_set_design_of_type_straight_bevel_gear_set_design(self) -> '_394.StraightBevelGearSetDesign':
        '''StraightBevelGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearSetDesign.__class__.__qualname__ != 'StraightBevelGearSetDesign':
            raise CastException('Failed to cast gear_set_design to StraightBevelGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new(_394.StraightBevelGearSetDesign)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign else None

    @property
    def gear_set_design_of_type_spiral_bevel_gear_set_design(self) -> '_395.SpiralBevelGearSetDesign':
        '''SpiralBevelGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearSetDesign.__class__.__qualname__ != 'SpiralBevelGearSetDesign':
            raise CastException('Failed to cast gear_set_design to SpiralBevelGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new(_395.SpiralBevelGearSetDesign)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign else None

    @property
    def gear_ratings(self) -> 'List[_329.GearDutyCycleRating]':
        '''List[GearDutyCycleRating]: 'GearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearRatings, constructor.new(_329.GearDutyCycleRating))
        return value

    @property
    def gear_duty_cycle_ratings(self) -> 'List[_329.GearDutyCycleRating]':
        '''List[GearDutyCycleRating]: 'GearDutyCycleRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearDutyCycleRatings, constructor.new(_329.GearDutyCycleRating))
        return value

    @property
    def gear_mesh_ratings(self) -> 'List[_343.MeshDutyCycleRating]':
        '''List[MeshDutyCycleRating]: 'GearMeshRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearMeshRatings, constructor.new(_343.MeshDutyCycleRating))
        return value

    @property
    def gear_mesh_duty_cycle_ratings(self) -> 'List[_343.MeshDutyCycleRating]':
        '''List[MeshDutyCycleRating]: 'GearMeshDutyCycleRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearMeshDutyCycleRatings, constructor.new(_343.MeshDutyCycleRating))
        return value
