'''_353.py

WormGearRating
'''


from mastapy.gears.gear_designs.worm import _475
from mastapy._internal import constructor
from mastapy.gears.rating import _337, _339
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Worm', 'WormGearRating')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearRating',)


class WormGearRating(_339.GearRating):
    '''WormGearRating

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_RATING
    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearRating.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def worm_gear(self) -> '_475.WormGearDesign':
        '''WormGearDesign: 'WormGear' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_475.WormGearDesign)(self.wrapped.WormGear) if self.wrapped.WormGear else None

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
