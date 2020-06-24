'''_588.py

BevelGearIsoMaterialDatabase
'''


from typing import Iterable

from mastapy.gears.materials import _587
from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_BEVEL_GEAR_ISO_MATERIAL_DATABASE = python_net_import('SMT.MastaAPI.Gears.Materials', 'BevelGearIsoMaterialDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelGearIsoMaterialDatabase',)


class BevelGearIsoMaterialDatabase(_1.APIBase):
    '''BevelGearIsoMaterialDatabase

    This is a mastapy class.
    '''

    TYPE = _BEVEL_GEAR_ISO_MATERIAL_DATABASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelGearIsoMaterialDatabase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def item(self) -> '_587.BevelGearISOMaterial':
        '''BevelGearISOMaterial: 'Item' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_587.BevelGearISOMaterial)(self.wrapped.Item) if self.wrapped.Item else None

    def create(self, name: 'str') -> '_587.BevelGearISOMaterial':
        ''' 'Create' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.gears.materials.BevelGearISOMaterial
        '''

        name = str(name)
        method_result = self.wrapped.Create(name if name else None)
        return constructor.new(_587.BevelGearISOMaterial)(method_result) if method_result else None

    def can_be_removed(self, bevel_gear_iso_material: '_587.BevelGearISOMaterial') -> 'bool':
        ''' 'CanBeRemoved' is the original name of this method.

        Args:
            bevel_gear_iso_material (mastapy.gears.materials.BevelGearISOMaterial)

        Returns:
            bool
        '''

        method_result = self.wrapped.CanBeRemoved(bevel_gear_iso_material.wrapped if bevel_gear_iso_material else None)
        return method_result

    def rename(self, bevel_gear_iso_material: '_587.BevelGearISOMaterial', new_name: 'str') -> 'bool':
        ''' 'Rename' is the original name of this method.

        Args:
            bevel_gear_iso_material (mastapy.gears.materials.BevelGearISOMaterial)
            new_name (str)

        Returns:
            bool
        '''

        new_name = str(new_name)
        method_result = self.wrapped.Rename(bevel_gear_iso_material.wrapped if bevel_gear_iso_material else None, new_name if new_name else None)
        return method_result

    def remove(self, bevel_gear_iso_material: '_587.BevelGearISOMaterial'):
        ''' 'Remove' is the original name of this method.

        Args:
            bevel_gear_iso_material (mastapy.gears.materials.BevelGearISOMaterial)
        '''

        self.wrapped.Remove(bevel_gear_iso_material.wrapped if bevel_gear_iso_material else None)

    def get_all_items(self) -> 'Iterable[_587.BevelGearISOMaterial]':
        ''' 'GetAllItems' is the original name of this method.

        Returns:
            Iterable[mastapy.gears.materials.BevelGearISOMaterial]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.GetAllItems(), constructor.new(_587.BevelGearISOMaterial))

    def save_changes(self, bevel_gear_iso_material: '_587.BevelGearISOMaterial'):
        ''' 'SaveChanges' is the original name of this method.

        Args:
            bevel_gear_iso_material (mastapy.gears.materials.BevelGearISOMaterial)
        '''

        self.wrapped.SaveChanges(bevel_gear_iso_material.wrapped if bevel_gear_iso_material else None)
