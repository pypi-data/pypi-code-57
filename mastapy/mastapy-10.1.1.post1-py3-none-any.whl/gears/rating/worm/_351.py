'''_351.py

WormGearDutyCycleRating
'''


from typing import List

from mastapy.gears.rating import _337, _329
from mastapy._internal import constructor, conversion
from mastapy.gears.rating.worm import _356, _353
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_DUTY_CYCLE_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Worm', 'WormGearDutyCycleRating')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearDutyCycleRating',)


class WormGearDutyCycleRating(_329.GearDutyCycleRating):
    '''WormGearDutyCycleRating

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_DUTY_CYCLE_RATING
    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearDutyCycleRating.TYPE'):
        super().__init__(instance_to_wrap)

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
    def gear_set_design_duty_cycle(self) -> '_356.WormGearSetDutyCycleRating':
        '''WormGearSetDutyCycleRating: 'GearSetDesignDutyCycle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_356.WormGearSetDutyCycleRating)(self.wrapped.GearSetDesignDutyCycle) if self.wrapped.GearSetDesignDutyCycle else None

    @property
    def worm_gear_set_design_duty_cycle(self) -> '_356.WormGearSetDutyCycleRating':
        '''WormGearSetDutyCycleRating: 'WormGearSetDesignDutyCycle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_356.WormGearSetDutyCycleRating)(self.wrapped.WormGearSetDesignDutyCycle) if self.wrapped.WormGearSetDesignDutyCycle else None

    @property
    def gear_ratings(self) -> 'List[_353.WormGearRating]':
        '''List[WormGearRating]: 'GearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearRatings, constructor.new(_353.WormGearRating))
        return value

    @property
    def worm_gear_ratings(self) -> 'List[_353.WormGearRating]':
        '''List[WormGearRating]: 'WormGearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearRatings, constructor.new(_353.WormGearRating))
        return value
