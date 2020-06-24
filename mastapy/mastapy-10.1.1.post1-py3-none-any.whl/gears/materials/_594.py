'''_594.py

CylindricalGearPlasticMaterialDatabase
'''


from typing import Iterable

from mastapy.gears.materials import _604
from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_PLASTIC_MATERIAL_DATABASE = python_net_import('SMT.MastaAPI.Gears.Materials', 'CylindricalGearPlasticMaterialDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearPlasticMaterialDatabase',)


class CylindricalGearPlasticMaterialDatabase(_1.APIBase):
    '''CylindricalGearPlasticMaterialDatabase

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_PLASTIC_MATERIAL_DATABASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearPlasticMaterialDatabase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def item(self) -> '_604.PlasticCylindricalGearMaterial':
        '''PlasticCylindricalGearMaterial: 'Item' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_604.PlasticCylindricalGearMaterial)(self.wrapped.Item) if self.wrapped.Item else None

    def create(self, name: 'str') -> '_604.PlasticCylindricalGearMaterial':
        ''' 'Create' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.gears.materials.PlasticCylindricalGearMaterial
        '''

        name = str(name)
        method_result = self.wrapped.Create(name if name else None)
        return constructor.new(_604.PlasticCylindricalGearMaterial)(method_result) if method_result else None

    def can_be_removed(self, plastic_cylindrical_gear_material: '_604.PlasticCylindricalGearMaterial') -> 'bool':
        ''' 'CanBeRemoved' is the original name of this method.

        Args:
            plastic_cylindrical_gear_material (mastapy.gears.materials.PlasticCylindricalGearMaterial)

        Returns:
            bool
        '''

        method_result = self.wrapped.CanBeRemoved(plastic_cylindrical_gear_material.wrapped if plastic_cylindrical_gear_material else None)
        return method_result

    def rename(self, plastic_cylindrical_gear_material: '_604.PlasticCylindricalGearMaterial', new_name: 'str') -> 'bool':
        ''' 'Rename' is the original name of this method.

        Args:
            plastic_cylindrical_gear_material (mastapy.gears.materials.PlasticCylindricalGearMaterial)
            new_name (str)

        Returns:
            bool
        '''

        new_name = str(new_name)
        method_result = self.wrapped.Rename(plastic_cylindrical_gear_material.wrapped if plastic_cylindrical_gear_material else None, new_name if new_name else None)
        return method_result

    def remove(self, plastic_cylindrical_gear_material: '_604.PlasticCylindricalGearMaterial'):
        ''' 'Remove' is the original name of this method.

        Args:
            plastic_cylindrical_gear_material (mastapy.gears.materials.PlasticCylindricalGearMaterial)
        '''

        self.wrapped.Remove(plastic_cylindrical_gear_material.wrapped if plastic_cylindrical_gear_material else None)

    def get_all_items(self) -> 'Iterable[_604.PlasticCylindricalGearMaterial]':
        ''' 'GetAllItems' is the original name of this method.

        Returns:
            Iterable[mastapy.gears.materials.PlasticCylindricalGearMaterial]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.GetAllItems(), constructor.new(_604.PlasticCylindricalGearMaterial))

    def save_changes(self, plastic_cylindrical_gear_material: '_604.PlasticCylindricalGearMaterial'):
        ''' 'SaveChanges' is the original name of this method.

        Args:
            plastic_cylindrical_gear_material (mastapy.gears.materials.PlasticCylindricalGearMaterial)
        '''

        self.wrapped.SaveChanges(plastic_cylindrical_gear_material.wrapped if plastic_cylindrical_gear_material else None)
