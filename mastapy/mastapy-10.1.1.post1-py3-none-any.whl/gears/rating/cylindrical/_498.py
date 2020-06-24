'''_498.py

MeshRatingForReports
'''


from mastapy._internal import constructor
from mastapy.gears.rating.cylindrical import _473
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_MESH_RATING_FOR_REPORTS = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical', 'MeshRatingForReports')


__docformat__ = 'restructuredtext en'
__all__ = ('MeshRatingForReports',)


class MeshRatingForReports(_1.APIBase):
    '''MeshRatingForReports

    This is a mastapy class.
    '''

    TYPE = _MESH_RATING_FOR_REPORTS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'MeshRatingForReports.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def safety_against_crack_initiation_without_influence_of_rim(self) -> 'float':
        '''float: 'SafetyAgainstCrackInitiationWithoutInfluenceOfRim' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SafetyAgainstCrackInitiationWithoutInfluenceOfRim

    @property
    def safety_against_crack_initiation_with_influence_of_rim(self) -> 'float':
        '''float: 'SafetyAgainstCrackInitiationWithInfluenceOfRim' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SafetyAgainstCrackInitiationWithInfluenceOfRim

    @property
    def cylindrical_gear_mesh_rating(self) -> '_473.CylindricalGearMeshRating':
        '''CylindricalGearMeshRating: 'CylindricalGearMeshRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_473.CylindricalGearMeshRating)(self.wrapped.CylindricalGearMeshRating) if self.wrapped.CylindricalGearMeshRating else None
