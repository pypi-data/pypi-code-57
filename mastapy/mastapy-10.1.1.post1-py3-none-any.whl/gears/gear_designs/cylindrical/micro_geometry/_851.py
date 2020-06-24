'''_851.py

CylindricalGearSetMicroGeometry
'''


from typing import List

from mastapy.gears.gear_designs.cylindrical import _786
from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.cylindrical.micro_geometry import _846, _844
from mastapy.gears.analysis import _962
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_MICRO_GEOMETRY = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry', 'CylindricalGearSetMicroGeometry')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetMicroGeometry',)


class CylindricalGearSetMicroGeometry(_962.GearSetImplementationDetail):
    '''CylindricalGearSetMicroGeometry

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_MICRO_GEOMETRY

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetMicroGeometry.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def cylindrical_gear_set_design(self) -> '_786.CylindricalGearSetDesign':
        '''CylindricalGearSetDesign: 'CylindricalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_786.CylindricalGearSetDesign)(self.wrapped.CylindricalGearSetDesign) if self.wrapped.CylindricalGearSetDesign else None

    @property
    def cylindrical_gear_micro_geometries(self) -> 'List[_846.CylindricalGearMicroGeometry]':
        '''List[CylindricalGearMicroGeometry]: 'CylindricalGearMicroGeometries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearMicroGeometries, constructor.new(_846.CylindricalGearMicroGeometry))
        return value

    @property
    def cylindrical_mesh_micro_geometries(self) -> 'List[_844.CylindricalGearMeshMicroGeometry]':
        '''List[CylindricalGearMeshMicroGeometry]: 'CylindricalMeshMicroGeometries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshMicroGeometries, constructor.new(_844.CylindricalGearMeshMicroGeometry))
        return value
