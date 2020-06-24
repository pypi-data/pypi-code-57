'''_254.py

CylindricalGearDutyCycleRating
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.rating import _161, _160
from mastapy.gears.rating.cylindrical import _263, _259, _273
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_DUTY_CYCLE_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical', 'CylindricalGearDutyCycleRating')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearDutyCycleRating',)


class CylindricalGearDutyCycleRating(_160.GearDutyCycleRating):
    '''CylindricalGearDutyCycleRating

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_DUTY_CYCLE_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearDutyCycleRating.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def safety_factor_against_permanent_deformation(self) -> 'float':
        '''float: 'SafetyFactorAgainstPermanentDeformation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SafetyFactorAgainstPermanentDeformation

    @property
    def safety_factor_against_permanent_deformation_with_influence_of_rim(self) -> 'float':
        '''float: 'SafetyFactorAgainstPermanentDeformationWithInfluenceOfRim' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SafetyFactorAgainstPermanentDeformationWithInfluenceOfRim

    @property
    def left_flank_rating(self) -> '_161.GearFlankRating':
        '''GearFlankRating: 'LeftFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_161.GearFlankRating)(self.wrapped.LeftFlankRating) if self.wrapped.LeftFlankRating else None

    @property
    def right_flank_rating(self) -> '_161.GearFlankRating':
        '''GearFlankRating: 'RightFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_161.GearFlankRating)(self.wrapped.RightFlankRating) if self.wrapped.RightFlankRating else None

    @property
    def gear_set_design_duty_cycle(self) -> '_263.CylindricalGearSetDutyCycleRating':
        '''CylindricalGearSetDutyCycleRating: 'GearSetDesignDutyCycle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_263.CylindricalGearSetDutyCycleRating)(self.wrapped.GearSetDesignDutyCycle) if self.wrapped.GearSetDesignDutyCycle else None

    @property
    def cylindrical_gear_set_design_duty_cycle(self) -> '_263.CylindricalGearSetDutyCycleRating':
        '''CylindricalGearSetDutyCycleRating: 'CylindricalGearSetDesignDutyCycle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_263.CylindricalGearSetDutyCycleRating)(self.wrapped.CylindricalGearSetDesignDutyCycle) if self.wrapped.CylindricalGearSetDesignDutyCycle else None

    @property
    def gear_ratings(self) -> 'List[_259.CylindricalGearRating]':
        '''List[CylindricalGearRating]: 'GearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearRatings, constructor.new(_259.CylindricalGearRating))
        return value

    @property
    def cylindrical_gear_ratings(self) -> 'List[_259.CylindricalGearRating]':
        '''List[CylindricalGearRating]: 'CylindricalGearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearRatings, constructor.new(_259.CylindricalGearRating))
        return value

    @property
    def cylindrical_gear_mesh_ratings(self) -> 'List[_273.MeshRatingForReports]':
        '''List[MeshRatingForReports]: 'CylindricalGearMeshRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearMeshRatings, constructor.new(_273.MeshRatingForReports))
        return value
