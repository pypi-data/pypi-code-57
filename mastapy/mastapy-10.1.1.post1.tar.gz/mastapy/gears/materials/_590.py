'''_590.py

BevelGearMaterialDatabase
'''


from typing import Iterable

from mastapy.gears.materials import _589
from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_BEVEL_GEAR_MATERIAL_DATABASE = python_net_import('SMT.MastaAPI.Gears.Materials', 'BevelGearMaterialDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelGearMaterialDatabase',)


class BevelGearMaterialDatabase(_1.APIBase):
    '''BevelGearMaterialDatabase

    This is a mastapy class.
    '''

    TYPE = _BEVEL_GEAR_MATERIAL_DATABASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelGearMaterialDatabase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def item(self) -> '_589.BevelGearMaterial':
        '''BevelGearMaterial: 'Item' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_589.BevelGearMaterial)(self.wrapped.Item) if self.wrapped.Item else None

    def create(self, name: 'str') -> '_589.BevelGearMaterial':
        ''' 'Create' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.gears.materials.BevelGearMaterial
        '''

        name = str(name)
        method_result = self.wrapped.Create(name if name else None)
        return constructor.new(_589.BevelGearMaterial)(method_result) if method_result else None

    def can_be_removed(self, bevel_gear_material: '_589.BevelGearMaterial') -> 'bool':
        ''' 'CanBeRemoved' is the original name of this method.

        Args:
            bevel_gear_material (mastapy.gears.materials.BevelGearMaterial)

        Returns:
            bool
        '''

        method_result = self.wrapped.CanBeRemoved(bevel_gear_material.wrapped if bevel_gear_material else None)
        return method_result

    def rename(self, bevel_gear_material: '_589.BevelGearMaterial', new_name: 'str') -> 'bool':
        ''' 'Rename' is the original name of this method.

        Args:
            bevel_gear_material (mastapy.gears.materials.BevelGearMaterial)
            new_name (str)

        Returns:
            bool
        '''

        new_name = str(new_name)
        method_result = self.wrapped.Rename(bevel_gear_material.wrapped if bevel_gear_material else None, new_name if new_name else None)
        return method_result

    def remove(self, bevel_gear_material: '_589.BevelGearMaterial'):
        ''' 'Remove' is the original name of this method.

        Args:
            bevel_gear_material (mastapy.gears.materials.BevelGearMaterial)
        '''

        self.wrapped.Remove(bevel_gear_material.wrapped if bevel_gear_material else None)

    def get_all_items(self) -> 'Iterable[_589.BevelGearMaterial]':
        ''' 'GetAllItems' is the original name of this method.

        Returns:
            Iterable[mastapy.gears.materials.BevelGearMaterial]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.GetAllItems(), constructor.new(_589.BevelGearMaterial))

    def save_changes(self, bevel_gear_material: '_589.BevelGearMaterial'):
        ''' 'SaveChanges' is the original name of this method.

        Args:
            bevel_gear_material (mastapy.gears.materials.BevelGearMaterial)
        '''

        self.wrapped.SaveChanges(bevel_gear_material.wrapped if bevel_gear_material else None)
