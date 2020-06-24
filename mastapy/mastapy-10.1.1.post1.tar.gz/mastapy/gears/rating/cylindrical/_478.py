'''_478.py

CylindricalGearRating
'''


from mastapy._internal import constructor
from mastapy.gears.rating import _337, _339
from mastapy.gears.rating.cylindrical import _497
from mastapy.gears.gear_designs.cylindrical import _546
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical', 'CylindricalGearRating')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearRating',)


class CylindricalGearRating(_339.GearRating):
    '''CylindricalGearRating

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_RATING
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearRating.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def damage_bending(self) -> 'float':
        '''float: 'DamageBending' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DamageBending

    @property
    def damage_contact(self) -> 'float':
        '''float: 'DamageContact' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DamageContact

    @property
    def worst_fatigue_fracture_safety_factor_with_influence_of_rim(self) -> 'float':
        '''float: 'WorstFatigueFractureSafetyFactorWithInfluenceOfRim' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.WorstFatigueFractureSafetyFactorWithInfluenceOfRim

    @property
    def worst_crack_initiation_safety_factor_with_influence_of_rim(self) -> 'float':
        '''float: 'WorstCrackInitiationSafetyFactorWithInfluenceOfRim' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.WorstCrackInitiationSafetyFactorWithInfluenceOfRim

    @property
    def worst_permanent_deformation_safety_factor_with_influence_of_rim(self) -> 'float':
        '''float: 'WorstPermanentDeformationSafetyFactorWithInfluenceOfRim' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.WorstPermanentDeformationSafetyFactorWithInfluenceOfRim

    @property
    def left_flank_rating(self) -> '_337.GearFlankRating':
        '''GearFlankRating: 'LeftFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_337.GearFlankRating)(self.wrapped.LeftFlankRating) if self.wrapped.LeftFlankRating else None

    @property
    def right_flank_rating(self) -> '_337.GearFlankRating':
        '''GearFlankRating: 'RightFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_337.GearFlankRating)(self.wrapped.RightFlankRating) if self.wrapped.RightFlankRating else None

    @property
    def vdi2737_safety_factor(self) -> '_497.VDI2737SafetyFactorReportingObject':
        '''VDI2737SafetyFactorReportingObject: 'VDI2737SafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_497.VDI2737SafetyFactorReportingObject)(self.wrapped.VDI2737SafetyFactor) if self.wrapped.VDI2737SafetyFactor else None

    @property
    def cylindrical_gear(self) -> '_546.CylindricalGearDesign':
        '''CylindricalGearDesign: 'CylindricalGear' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_546.CylindricalGearDesign)(self.wrapped.CylindricalGear) if self.wrapped.CylindricalGear else None
