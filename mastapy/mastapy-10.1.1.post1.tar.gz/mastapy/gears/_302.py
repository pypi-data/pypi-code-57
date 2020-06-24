'''_302.py

GearSetOptimisationResult
'''


from mastapy.gears.gear_designs import _375
from mastapy._internal import constructor
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
from mastapy.gears.rating import _326
from mastapy.gears.rating.worm import _356, _361
from mastapy.gears.rating.face import _357, _396
from mastapy.gears.rating.cylindrical import _358, _397
from mastapy.gears.rating.conical import _359
from mastapy.gears.rating.concept import _360, _398
from mastapy.gears.rating.straight_bevel_diff import _399
from mastapy.gears.rating.klingelnberg_spiral_bevel import _400
from mastapy.gears.rating.klingelnberg_hypoid import _401
from mastapy.gears.rating.hypoid import _402
from mastapy.gears.rating.zerol_bevel import _350
from mastapy.gears.rating.straight_bevel import _403
from mastapy.gears.rating.spiral_bevel import _404
from mastapy.math_utility.optimisation import _405
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_GEAR_SET_OPTIMISATION_RESULT = python_net_import('SMT.MastaAPI.Gears', 'GearSetOptimisationResult')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetOptimisationResult',)


class GearSetOptimisationResult(_1.APIBase):
    '''GearSetOptimisationResult

    This is a mastapy class.
    '''

    TYPE = _GEAR_SET_OPTIMISATION_RESULT
    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearSetOptimisationResult.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def gear_set(self) -> '_375.GearSetDesign':
        '''GearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_375.GearSetDesign)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_worm_gear_set_design(self) -> '_384.WormGearSetDesign':
        '''WormGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearSet.__class__.__qualname__ != 'WormGearSetDesign':
            raise CastException('Failed to cast gear_set to WormGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new(_384.WormGearSetDesign)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_face_gear_set_design(self) -> '_385.FaceGearSetDesign':
        '''FaceGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearSet.__class__.__qualname__ != 'FaceGearSetDesign':
            raise CastException('Failed to cast gear_set to FaceGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new(_385.FaceGearSetDesign)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_cylindrical_gear_set_design(self) -> '_386.CylindricalGearSetDesign':
        '''CylindricalGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearSet.__class__.__qualname__ != 'CylindricalGearSetDesign':
            raise CastException('Failed to cast gear_set to CylindricalGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new(_386.CylindricalGearSetDesign)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_concept_gear_set_design(self) -> '_387.ConceptGearSetDesign':
        '''ConceptGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearSet.__class__.__qualname__ != 'ConceptGearSetDesign':
            raise CastException('Failed to cast gear_set to ConceptGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new(_387.ConceptGearSetDesign)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_cylindrical_planetary_gear_set_design(self) -> '_388.CylindricalPlanetaryGearSetDesign':
        '''CylindricalPlanetaryGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearSet.__class__.__qualname__ != 'CylindricalPlanetaryGearSetDesign':
            raise CastException('Failed to cast gear_set to CylindricalPlanetaryGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new(_388.CylindricalPlanetaryGearSetDesign)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_design(self) -> '_389.KlingelnbergCycloPalloidSpiralBevelGearSetDesign':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearSet.__class__.__qualname__ != 'KlingelnbergCycloPalloidSpiralBevelGearSetDesign':
            raise CastException('Failed to cast gear_set to KlingelnbergCycloPalloidSpiralBevelGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new(_389.KlingelnbergCycloPalloidSpiralBevelGearSetDesign)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set_design(self) -> '_390.KlingelnbergCycloPalloidHypoidGearSetDesign':
        '''KlingelnbergCycloPalloidHypoidGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearSet.__class__.__qualname__ != 'KlingelnbergCycloPalloidHypoidGearSetDesign':
            raise CastException('Failed to cast gear_set to KlingelnbergCycloPalloidHypoidGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new(_390.KlingelnbergCycloPalloidHypoidGearSetDesign)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_hypoid_gear_set_design(self) -> '_391.HypoidGearSetDesign':
        '''HypoidGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearSet.__class__.__qualname__ != 'HypoidGearSetDesign':
            raise CastException('Failed to cast gear_set to HypoidGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new(_391.HypoidGearSetDesign)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_zerol_bevel_gear_set_design(self) -> '_392.ZerolBevelGearSetDesign':
        '''ZerolBevelGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearSet.__class__.__qualname__ != 'ZerolBevelGearSetDesign':
            raise CastException('Failed to cast gear_set to ZerolBevelGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new(_392.ZerolBevelGearSetDesign)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_straight_bevel_diff_gear_set_design(self) -> '_393.StraightBevelDiffGearSetDesign':
        '''StraightBevelDiffGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearSet.__class__.__qualname__ != 'StraightBevelDiffGearSetDesign':
            raise CastException('Failed to cast gear_set to StraightBevelDiffGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new(_393.StraightBevelDiffGearSetDesign)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_straight_bevel_gear_set_design(self) -> '_394.StraightBevelGearSetDesign':
        '''StraightBevelGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearSet.__class__.__qualname__ != 'StraightBevelGearSetDesign':
            raise CastException('Failed to cast gear_set to StraightBevelGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new(_394.StraightBevelGearSetDesign)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_spiral_bevel_gear_set_design(self) -> '_395.SpiralBevelGearSetDesign':
        '''SpiralBevelGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearSet.__class__.__qualname__ != 'SpiralBevelGearSetDesign':
            raise CastException('Failed to cast gear_set to SpiralBevelGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new(_395.SpiralBevelGearSetDesign)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def rating(self) -> '_326.AbstractGearSetRating':
        '''AbstractGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_326.AbstractGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_worm_gear_set_duty_cycle_rating(self) -> '_356.WormGearSetDutyCycleRating':
        '''WormGearSetDutyCycleRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Rating.__class__.__qualname__ != 'WormGearSetDutyCycleRating':
            raise CastException('Failed to cast rating to WormGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new(_356.WormGearSetDutyCycleRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_face_gear_set_duty_cycle_rating(self) -> '_357.FaceGearSetDutyCycleRating':
        '''FaceGearSetDutyCycleRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Rating.__class__.__qualname__ != 'FaceGearSetDutyCycleRating':
            raise CastException('Failed to cast rating to FaceGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new(_357.FaceGearSetDutyCycleRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_cylindrical_gear_set_duty_cycle_rating(self) -> '_358.CylindricalGearSetDutyCycleRating':
        '''CylindricalGearSetDutyCycleRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Rating.__class__.__qualname__ != 'CylindricalGearSetDutyCycleRating':
            raise CastException('Failed to cast rating to CylindricalGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new(_358.CylindricalGearSetDutyCycleRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_conical_gear_set_duty_cycle_rating(self) -> '_359.ConicalGearSetDutyCycleRating':
        '''ConicalGearSetDutyCycleRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Rating.__class__.__qualname__ != 'ConicalGearSetDutyCycleRating':
            raise CastException('Failed to cast rating to ConicalGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new(_359.ConicalGearSetDutyCycleRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_concept_gear_set_duty_cycle_rating(self) -> '_360.ConceptGearSetDutyCycleRating':
        '''ConceptGearSetDutyCycleRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Rating.__class__.__qualname__ != 'ConceptGearSetDutyCycleRating':
            raise CastException('Failed to cast rating to ConceptGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new(_360.ConceptGearSetDutyCycleRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_worm_gear_set_rating(self) -> '_361.WormGearSetRating':
        '''WormGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Rating.__class__.__qualname__ != 'WormGearSetRating':
            raise CastException('Failed to cast rating to WormGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new(_361.WormGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_face_gear_set_rating(self) -> '_396.FaceGearSetRating':
        '''FaceGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Rating.__class__.__qualname__ != 'FaceGearSetRating':
            raise CastException('Failed to cast rating to FaceGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new(_396.FaceGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_cylindrical_gear_set_rating(self) -> '_397.CylindricalGearSetRating':
        '''CylindricalGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Rating.__class__.__qualname__ != 'CylindricalGearSetRating':
            raise CastException('Failed to cast rating to CylindricalGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new(_397.CylindricalGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_concept_gear_set_rating(self) -> '_398.ConceptGearSetRating':
        '''ConceptGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Rating.__class__.__qualname__ != 'ConceptGearSetRating':
            raise CastException('Failed to cast rating to ConceptGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new(_398.ConceptGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_straight_bevel_diff_gear_set_rating(self) -> '_399.StraightBevelDiffGearSetRating':
        '''StraightBevelDiffGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Rating.__class__.__qualname__ != 'StraightBevelDiffGearSetRating':
            raise CastException('Failed to cast rating to StraightBevelDiffGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new(_399.StraightBevelDiffGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_rating(self) -> '_400.KlingelnbergCycloPalloidSpiralBevelGearSetRating':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Rating.__class__.__qualname__ != 'KlingelnbergCycloPalloidSpiralBevelGearSetRating':
            raise CastException('Failed to cast rating to KlingelnbergCycloPalloidSpiralBevelGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new(_400.KlingelnbergCycloPalloidSpiralBevelGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set_rating(self) -> '_401.KlingelnbergCycloPalloidHypoidGearSetRating':
        '''KlingelnbergCycloPalloidHypoidGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Rating.__class__.__qualname__ != 'KlingelnbergCycloPalloidHypoidGearSetRating':
            raise CastException('Failed to cast rating to KlingelnbergCycloPalloidHypoidGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new(_401.KlingelnbergCycloPalloidHypoidGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_hypoid_gear_set_rating(self) -> '_402.HypoidGearSetRating':
        '''HypoidGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Rating.__class__.__qualname__ != 'HypoidGearSetRating':
            raise CastException('Failed to cast rating to HypoidGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new(_402.HypoidGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_zerol_bevel_gear_set_rating(self) -> '_350.ZerolBevelGearSetRating':
        '''ZerolBevelGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Rating.__class__.__qualname__ != 'ZerolBevelGearSetRating':
            raise CastException('Failed to cast rating to ZerolBevelGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new(_350.ZerolBevelGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_straight_bevel_gear_set_rating(self) -> '_403.StraightBevelGearSetRating':
        '''StraightBevelGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Rating.__class__.__qualname__ != 'StraightBevelGearSetRating':
            raise CastException('Failed to cast rating to StraightBevelGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new(_403.StraightBevelGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_spiral_bevel_gear_set_rating(self) -> '_404.SpiralBevelGearSetRating':
        '''SpiralBevelGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Rating.__class__.__qualname__ != 'SpiralBevelGearSetRating':
            raise CastException('Failed to cast rating to SpiralBevelGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new(_404.SpiralBevelGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def optimisation_history(self) -> '_405.OptimisationHistory':
        '''OptimisationHistory: 'OptimisationHistory' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_405.OptimisationHistory)(self.wrapped.OptimisationHistory) if self.wrapped.OptimisationHistory else None

    @property
    def is_optimized(self) -> 'bool':
        '''bool: 'IsOptimized' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IsOptimized
