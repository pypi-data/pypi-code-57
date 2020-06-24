'''_333.py

ConceptGearDutyCycleRating
'''


from mastapy.gears.rating import _161, _160
from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_DUTY_CYCLE_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Concept', 'ConceptGearDutyCycleRating')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearDutyCycleRating',)


class ConceptGearDutyCycleRating(_160.GearDutyCycleRating):
    '''ConceptGearDutyCycleRating

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_DUTY_CYCLE_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearDutyCycleRating.TYPE'):
        super().__init__(instance_to_wrap)

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
