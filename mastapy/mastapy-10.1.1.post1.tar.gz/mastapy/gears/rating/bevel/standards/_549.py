'''_549.py

AGMASpiralBevelMeshSingleFlankRating
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy._internal.implicit import overridable
from mastapy.gears.rating.bevel.standards import _548, _556
from mastapy._internal.python_net import python_net_import

_AGMA_SPIRAL_BEVEL_MESH_SINGLE_FLANK_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Bevel.Standards', 'AGMASpiralBevelMeshSingleFlankRating')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMASpiralBevelMeshSingleFlankRating',)


class AGMASpiralBevelMeshSingleFlankRating(_556.SpiralBevelMeshSingleFlankRating):
    '''AGMASpiralBevelMeshSingleFlankRating

    This is a mastapy class.
    '''

    TYPE = _AGMA_SPIRAL_BEVEL_MESH_SINGLE_FLANK_RATING
    __hash__ = None

    def __init__(self, instance_to_wrap: 'AGMASpiralBevelMeshSingleFlankRating.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def rating_standard_name(self) -> 'str':
        '''str: 'RatingStandardName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RatingStandardName

    @property
    def crowning_factor(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'CrowningFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(overridable.Overridable_float)(self.wrapped.CrowningFactor) if self.wrapped.CrowningFactor else None

    @property
    def gear_single_flank_ratings(self) -> 'List[_548.AGMASpiralBevelGearSingleFlankRating]':
        '''List[AGMASpiralBevelGearSingleFlankRating]: 'GearSingleFlankRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearSingleFlankRatings, constructor.new(_548.AGMASpiralBevelGearSingleFlankRating))
        return value

    @property
    def agma_bevel_gear_single_flank_ratings(self) -> 'List[_548.AGMASpiralBevelGearSingleFlankRating]':
        '''List[AGMASpiralBevelGearSingleFlankRating]: 'AGMABevelGearSingleFlankRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AGMABevelGearSingleFlankRatings, constructor.new(_548.AGMASpiralBevelGearSingleFlankRating))
        return value
