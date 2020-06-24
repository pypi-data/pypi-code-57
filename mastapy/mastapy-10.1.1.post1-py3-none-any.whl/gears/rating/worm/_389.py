'''_389.py

WormGearRating
'''


from mastapy.gears.gear_designs.worm import _455
from mastapy._internal import constructor
from mastapy.gears.rating import _334, _336
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Worm', 'WormGearRating')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearRating',)


class WormGearRating(_336.GearRating):
    '''WormGearRating

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_RATING
    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearRating.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def worm_gear(self) -> '_455.WormGearDesign':
        '''WormGearDesign: 'WormGear' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_455.WormGearDesign)(self.wrapped.WormGear) if self.wrapped.WormGear else None

    @property
    def left_flank_rating(self) -> '_334.GearFlankRating':
        '''GearFlankRating: 'LeftFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_334.GearFlankRating)(self.wrapped.LeftFlankRating) if self.wrapped.LeftFlankRating else None

    @property
    def right_flank_rating(self) -> '_334.GearFlankRating':
        '''GearFlankRating: 'RightFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_334.GearFlankRating)(self.wrapped.RightFlankRating) if self.wrapped.RightFlankRating else None
