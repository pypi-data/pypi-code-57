'''_176.py

WormGearRating
'''


from mastapy.gears.gear_designs.worm import _722
from mastapy._internal import constructor
from mastapy.gears.rating import _161, _163
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Worm', 'WormGearRating')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearRating',)


class WormGearRating(_163.GearRating):
    '''WormGearRating

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearRating.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def worm_gear(self) -> '_722.WormGearDesign':
        '''WormGearDesign: 'WormGear' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_722.WormGearDesign)(self.wrapped.WormGear) if self.wrapped.WormGear else None

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
