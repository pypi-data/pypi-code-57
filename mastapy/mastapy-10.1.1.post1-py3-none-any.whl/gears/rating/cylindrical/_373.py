'''_373.py

CylindricalGearSetRating
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.rating.cylindrical import _20, _475, _477
from mastapy.gears.rating.cylindrical.optimisation import _513
from mastapy.gears.gear_designs.cylindrical import _356
from mastapy.gears.rating.cylindrical.vdi import _501
from mastapy.gears.rating import _338
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical', 'CylindricalGearSetRating')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetRating',)


class CylindricalGearSetRating(_338.GearSetRating):
    '''CylindricalGearSetRating

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_RATING
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetRating.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def rating_standard_name(self) -> 'str':
        '''str: 'RatingStandardName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RatingStandardName

    @property
    def rating_settings(self) -> '_20.CylindricalGearRatingSettings':
        '''CylindricalGearRatingSettings: 'RatingSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_20.CylindricalGearRatingSettings)(self.wrapped.RatingSettings) if self.wrapped.RatingSettings else None

    @property
    def optimisations(self) -> '_513.CylindricalGearSetRatingOptimisationHelper':
        '''CylindricalGearSetRatingOptimisationHelper: 'Optimisations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_513.CylindricalGearSetRatingOptimisationHelper)(self.wrapped.Optimisations) if self.wrapped.Optimisations else None

    @property
    def cylindrical_gear_set(self) -> '_356.CylindricalGearSetDesign':
        '''CylindricalGearSetDesign: 'CylindricalGearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_356.CylindricalGearSetDesign)(self.wrapped.CylindricalGearSet) if self.wrapped.CylindricalGearSet else None

    @property
    def vdi_cylindrical_gear_single_flank_ratings(self) -> 'List[_501.VDI2737InternalGearSingleFlankRating]':
        '''List[VDI2737InternalGearSingleFlankRating]: 'VDICylindricalGearSingleFlankRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.VDICylindricalGearSingleFlankRatings, constructor.new(_501.VDI2737InternalGearSingleFlankRating))
        return value

    @property
    def cylindrical_mesh_ratings(self) -> 'List[_475.CylindricalGearMeshRating]':
        '''List[CylindricalGearMeshRating]: 'CylindricalMeshRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshRatings, constructor.new(_475.CylindricalGearMeshRating))
        return value

    @property
    def gear_ratings(self) -> 'List[_477.CylindricalGearRating]':
        '''List[CylindricalGearRating]: 'GearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearRatings, constructor.new(_477.CylindricalGearRating))
        return value

    @property
    def cylindrical_gear_ratings(self) -> 'List[_477.CylindricalGearRating]':
        '''List[CylindricalGearRating]: 'CylindricalGearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearRatings, constructor.new(_477.CylindricalGearRating))
        return value
