'''_336.py

ConceptGearRating
'''


from mastapy.gears.rating import _161, _163
from mastapy._internal import constructor
from mastapy.gears.gear_designs.concept import _910
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Concept', 'ConceptGearRating')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearRating',)


class ConceptGearRating(_163.GearRating):
    '''ConceptGearRating

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearRating.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def concave_flank_rating(self) -> '_161.GearFlankRating':
        '''GearFlankRating: 'ConcaveFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_161.GearFlankRating)(self.wrapped.ConcaveFlankRating) if self.wrapped.ConcaveFlankRating else None

    @property
    def convex_flank_rating(self) -> '_161.GearFlankRating':
        '''GearFlankRating: 'ConvexFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_161.GearFlankRating)(self.wrapped.ConvexFlankRating) if self.wrapped.ConvexFlankRating else None

    @property
    def concept_gear(self) -> '_910.ConceptGearDesign':
        '''ConceptGearDesign: 'ConceptGear' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_910.ConceptGearDesign)(self.wrapped.ConceptGear) if self.wrapped.ConceptGear else None
