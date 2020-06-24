'''_415.py

SpiralBevelGearMeshRating
'''


from typing import List

from mastapy.gears.gear_designs.spiral_bevel import _441
from mastapy._internal import constructor, conversion
from mastapy.gears.rating.spiral_bevel import _416
from mastapy.gears.rating.bevel import _426
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_MESH_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.SpiralBevel', 'SpiralBevelGearMeshRating')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearMeshRating',)


class SpiralBevelGearMeshRating(_426.BevelGearMeshRating):
    '''SpiralBevelGearMeshRating

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_MESH_RATING
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearMeshRating.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def spiral_bevel_gear_mesh(self) -> '_441.SpiralBevelGearMeshDesign':
        '''SpiralBevelGearMeshDesign: 'SpiralBevelGearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_441.SpiralBevelGearMeshDesign)(self.wrapped.SpiralBevelGearMesh) if self.wrapped.SpiralBevelGearMesh else None

    @property
    def spiral_bevel_gear_ratings(self) -> 'List[_416.SpiralBevelGearRating]':
        '''List[SpiralBevelGearRating]: 'SpiralBevelGearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearRatings, constructor.new(_416.SpiralBevelGearRating))
        return value
