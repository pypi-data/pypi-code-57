'''_339.py

BevelGearMeshRating
'''


from typing import List

from mastapy._internal.implicit import overridable
from mastapy._internal import constructor, conversion
from mastapy.gears.rating.bevel.standards import _345, _343
from mastapy.gears.rating.iso_10300 import _227, _225
from mastapy.gears.rating.conical import _330
from mastapy.gears.rating.agma_gleason_conical import _350
from mastapy._internal.python_net import python_net_import

_BEVEL_GEAR_MESH_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Bevel', 'BevelGearMeshRating')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelGearMeshRating',)


class BevelGearMeshRating(_350.AGMAGleasonConicalGearMeshRating):
    '''BevelGearMeshRating

    This is a mastapy class.
    '''

    TYPE = _BEVEL_GEAR_MESH_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelGearMeshRating.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def size_factor_bending(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'SizeFactorBending' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(overridable.Overridable_float)(self.wrapped.SizeFactorBending) if self.wrapped.SizeFactorBending else None

    @property
    def size_factor_contact(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'SizeFactorContact' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(overridable.Overridable_float)(self.wrapped.SizeFactorContact) if self.wrapped.SizeFactorContact else None

    @property
    def gleason_bevel_mesh_single_flank_rating(self) -> '_345.GleasonSpiralBevelMeshSingleFlankRating':
        '''GleasonSpiralBevelMeshSingleFlankRating: 'GleasonBevelMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_345.GleasonSpiralBevelMeshSingleFlankRating)(self.wrapped.GleasonBevelMeshSingleFlankRating) if self.wrapped.GleasonBevelMeshSingleFlankRating else None

    @property
    def agma_bevel_mesh_single_flank_rating(self) -> '_343.AGMASpiralBevelMeshSingleFlankRating':
        '''AGMASpiralBevelMeshSingleFlankRating: 'AGMABevelMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_343.AGMASpiralBevelMeshSingleFlankRating)(self.wrapped.AGMABevelMeshSingleFlankRating) if self.wrapped.AGMABevelMeshSingleFlankRating else None

    @property
    def iso10300_bevel_mesh_single_flank_rating_method_b1(self) -> '_227.ISO10300MeshSingleFlankRatingMethodB1':
        '''ISO10300MeshSingleFlankRatingMethodB1: 'ISO10300BevelMeshSingleFlankRatingMethodB1' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_227.ISO10300MeshSingleFlankRatingMethodB1)(self.wrapped.ISO10300BevelMeshSingleFlankRatingMethodB1) if self.wrapped.ISO10300BevelMeshSingleFlankRatingMethodB1 else None

    @property
    def iso10300_bevel_mesh_single_flank_rating_method_b2(self) -> '_225.Iso10300MeshSingleFlankRatingBevelMethodB2':
        '''Iso10300MeshSingleFlankRatingBevelMethodB2: 'ISO10300BevelMeshSingleFlankRatingMethodB2' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_225.Iso10300MeshSingleFlankRatingBevelMethodB2)(self.wrapped.ISO10300BevelMeshSingleFlankRatingMethodB2) if self.wrapped.ISO10300BevelMeshSingleFlankRatingMethodB2 else None

    @property
    def meshed_gears(self) -> 'List[_330.ConicalMeshedGearRating]':
        '''List[ConicalMeshedGearRating]: 'MeshedGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshedGears, constructor.new(_330.ConicalMeshedGearRating))
        return value

    @property
    def gears_in_mesh(self) -> 'List[_330.ConicalMeshedGearRating]':
        '''List[ConicalMeshedGearRating]: 'GearsInMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearsInMesh, constructor.new(_330.ConicalMeshedGearRating))
        return value
