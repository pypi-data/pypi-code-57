'''_399.py

StraightBevelDiffGearSetRating
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.straight_bevel_diff import _393
from mastapy.gears.rating.straight_bevel_diff import _410, _411
from mastapy.gears.rating.conical import _461
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.StraightBevelDiff', 'StraightBevelDiffGearSetRating')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetRating',)


class StraightBevelDiffGearSetRating(_461.ConicalGearSetRating):
    '''StraightBevelDiffGearSetRating

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_RATING
    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetRating.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def rating(self) -> 'str':
        '''str: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Rating

    @property
    def straight_bevel_diff_gear_set(self) -> '_393.StraightBevelDiffGearSetDesign':
        '''StraightBevelDiffGearSetDesign: 'StraightBevelDiffGearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_393.StraightBevelDiffGearSetDesign)(self.wrapped.StraightBevelDiffGearSet) if self.wrapped.StraightBevelDiffGearSet else None

    @property
    def straight_bevel_diff_mesh_ratings(self) -> 'List[_410.StraightBevelDiffGearMeshRating]':
        '''List[StraightBevelDiffGearMeshRating]: 'StraightBevelDiffMeshRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshRatings, constructor.new(_410.StraightBevelDiffGearMeshRating))
        return value

    @property
    def straight_bevel_diff_gear_ratings(self) -> 'List[_411.StraightBevelDiffGearRating]':
        '''List[StraightBevelDiffGearRating]: 'StraightBevelDiffGearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearRatings, constructor.new(_411.StraightBevelDiffGearRating))
        return value
