'''_379.py

ZerolBevelGearSetRating
'''


from typing import List

from mastapy.gears.gear_designs.zerol_bevel import _362
from mastapy._internal import constructor, conversion
from mastapy.gears.rating.zerol_bevel import _385, _386
from mastapy.gears.rating.bevel import _443
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.ZerolBevel', 'ZerolBevelGearSetRating')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetRating',)


class ZerolBevelGearSetRating(_443.BevelGearSetRating):
    '''ZerolBevelGearSetRating

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_RATING
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetRating.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def zerol_bevel_gear_set(self) -> '_362.ZerolBevelGearSetDesign':
        '''ZerolBevelGearSetDesign: 'ZerolBevelGearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_362.ZerolBevelGearSetDesign)(self.wrapped.ZerolBevelGearSet) if self.wrapped.ZerolBevelGearSet else None

    @property
    def zerol_bevel_mesh_ratings(self) -> 'List[_385.ZerolBevelGearMeshRating]':
        '''List[ZerolBevelGearMeshRating]: 'ZerolBevelMeshRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshRatings, constructor.new(_385.ZerolBevelGearMeshRating))
        return value

    @property
    def zerol_bevel_gear_ratings(self) -> 'List[_386.ZerolBevelGearRating]':
        '''List[ZerolBevelGearRating]: 'ZerolBevelGearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearRatings, constructor.new(_386.ZerolBevelGearRating))
        return value
