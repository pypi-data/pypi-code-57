'''_844.py

CylindricalGearMeshMicroGeometry
'''


from typing import List

from mastapy.gears.gear_designs.cylindrical import _784, _781
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.gears.gear_designs.cylindrical.micro_geometry import _851, _846
from mastapy.gears.analysis import _956
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_MICRO_GEOMETRY = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry', 'CylindricalGearMeshMicroGeometry')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshMicroGeometry',)


class CylindricalGearMeshMicroGeometry(_956.GearMeshImplementationDetail):
    '''CylindricalGearMeshMicroGeometry

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MESH_MICRO_GEOMETRY

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshMicroGeometry.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def profile_measured_as(self) -> '_784.CylindricalGearProfileMeasurementType':
        '''CylindricalGearProfileMeasurementType: 'ProfileMeasuredAs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.ProfileMeasuredAs)
        return constructor.new(_784.CylindricalGearProfileMeasurementType)(value) if value else None

    @property
    def cylindrical_mesh(self) -> '_781.CylindricalGearMeshDesign':
        '''CylindricalGearMeshDesign: 'CylindricalMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_781.CylindricalGearMeshDesign)(self.wrapped.CylindricalMesh) if self.wrapped.CylindricalMesh else None

    @property
    def cylindrical_gear_set_micro_geometry(self) -> '_851.CylindricalGearSetMicroGeometry':
        '''CylindricalGearSetMicroGeometry: 'CylindricalGearSetMicroGeometry' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_851.CylindricalGearSetMicroGeometry)(self.wrapped.CylindricalGearSetMicroGeometry) if self.wrapped.CylindricalGearSetMicroGeometry else None

    @property
    def cylindrical_gear_micro_geometries(self) -> 'List[_846.CylindricalGearMicroGeometry]':
        '''List[CylindricalGearMicroGeometry]: 'CylindricalGearMicroGeometries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearMicroGeometries, constructor.new(_846.CylindricalGearMicroGeometry))
        return value

    @property
    def gear_a(self) -> '_846.CylindricalGearMicroGeometry':
        '''CylindricalGearMicroGeometry: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_846.CylindricalGearMicroGeometry)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_b(self) -> '_846.CylindricalGearMicroGeometry':
        '''CylindricalGearMicroGeometry: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_846.CylindricalGearMicroGeometry)(self.wrapped.GearB) if self.wrapped.GearB else None
