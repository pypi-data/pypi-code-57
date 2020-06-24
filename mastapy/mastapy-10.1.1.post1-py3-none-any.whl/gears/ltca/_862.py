'''_862.py

GearMeshLoadedContactPoint
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_GEAR_MESH_LOADED_CONTACT_POINT = python_net_import('SMT.MastaAPI.Gears.LTCA', 'GearMeshLoadedContactPoint')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMeshLoadedContactPoint',)


class GearMeshLoadedContactPoint(_1.APIBase):
    '''GearMeshLoadedContactPoint

    This is a mastapy class.
    '''

    TYPE = _GEAR_MESH_LOADED_CONTACT_POINT
    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearMeshLoadedContactPoint.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def force_unit_length(self) -> 'float':
        '''float: 'ForceUnitLength' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ForceUnitLength

    @property
    def strip_length(self) -> 'float':
        '''float: 'StripLength' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StripLength

    @property
    def total_deflection_for_mesh(self) -> 'float':
        '''float: 'TotalDeflectionForMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalDeflectionForMesh

    @property
    def gaps_between_flanks_in_transverse_plane(self) -> 'float':
        '''float: 'GapsBetweenFlanksInTransversePlane' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.GapsBetweenFlanksInTransversePlane

    @property
    def contact_point_index(self) -> 'int':
        '''int: 'ContactPointIndex' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ContactPointIndex

    @property
    def contact_line_index(self) -> 'int':
        '''int: 'ContactLineIndex' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ContactLineIndex

    @property
    def mesh_position_index(self) -> 'int':
        '''int: 'MeshPositionIndex' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MeshPositionIndex

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def contact_pressure(self) -> 'float':
        '''float: 'ContactPressure' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ContactPressure

    @property
    def max_sheer_stress(self) -> 'float':
        '''float: 'MaxSheerStress' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaxSheerStress

    @property
    def depth_of_max_sheer_stress(self) -> 'float':
        '''float: 'DepthOfMaxSheerStress' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DepthOfMaxSheerStress

    @property
    def hertzian_contact_half_width(self) -> 'float':
        '''float: 'HertzianContactHalfWidth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HertzianContactHalfWidth
