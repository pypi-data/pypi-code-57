'''_458.py

FaceGearDutyCycleRating
'''


from mastapy.gears.rating import _335, _334
from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_DUTY_CYCLE_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Face', 'FaceGearDutyCycleRating')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearDutyCycleRating',)


class FaceGearDutyCycleRating(_334.GearDutyCycleRating):
    '''FaceGearDutyCycleRating

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_DUTY_CYCLE_RATING
    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearDutyCycleRating.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def left_flank_rating(self) -> '_335.GearFlankRating':
        '''GearFlankRating: 'LeftFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_335.GearFlankRating)(self.wrapped.LeftFlankRating) if self.wrapped.LeftFlankRating else None

    @property
    def right_flank_rating(self) -> '_335.GearFlankRating':
        '''GearFlankRating: 'RightFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_335.GearFlankRating)(self.wrapped.RightFlankRating) if self.wrapped.RightFlankRating else None
