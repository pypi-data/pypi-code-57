'''_607.py

RawMaterialDatabase
'''


from typing import Iterable

from mastapy.gears.materials import _606
from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_RAW_MATERIAL_DATABASE = python_net_import('SMT.MastaAPI.Gears.Materials', 'RawMaterialDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('RawMaterialDatabase',)


class RawMaterialDatabase(_1.APIBase):
    '''RawMaterialDatabase

    This is a mastapy class.
    '''

    TYPE = _RAW_MATERIAL_DATABASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'RawMaterialDatabase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def item(self) -> '_606.RawMaterial':
        '''RawMaterial: 'Item' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_606.RawMaterial)(self.wrapped.Item) if self.wrapped.Item else None

    def create(self, name: 'str') -> '_606.RawMaterial':
        ''' 'Create' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.gears.materials.RawMaterial
        '''

        name = str(name)
        method_result = self.wrapped.Create(name if name else None)
        return constructor.new(_606.RawMaterial)(method_result) if method_result else None

    def can_be_removed(self, raw_material: '_606.RawMaterial') -> 'bool':
        ''' 'CanBeRemoved' is the original name of this method.

        Args:
            raw_material (mastapy.gears.materials.RawMaterial)

        Returns:
            bool
        '''

        method_result = self.wrapped.CanBeRemoved(raw_material.wrapped if raw_material else None)
        return method_result

    def rename(self, raw_material: '_606.RawMaterial', new_name: 'str') -> 'bool':
        ''' 'Rename' is the original name of this method.

        Args:
            raw_material (mastapy.gears.materials.RawMaterial)
            new_name (str)

        Returns:
            bool
        '''

        new_name = str(new_name)
        method_result = self.wrapped.Rename(raw_material.wrapped if raw_material else None, new_name if new_name else None)
        return method_result

    def remove(self, raw_material: '_606.RawMaterial'):
        ''' 'Remove' is the original name of this method.

        Args:
            raw_material (mastapy.gears.materials.RawMaterial)
        '''

        self.wrapped.Remove(raw_material.wrapped if raw_material else None)

    def get_all_items(self) -> 'Iterable[_606.RawMaterial]':
        ''' 'GetAllItems' is the original name of this method.

        Returns:
            Iterable[mastapy.gears.materials.RawMaterial]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.GetAllItems(), constructor.new(_606.RawMaterial))

    def save_changes(self, raw_material: '_606.RawMaterial'):
        ''' 'SaveChanges' is the original name of this method.

        Args:
            raw_material (mastapy.gears.materials.RawMaterial)
        '''

        self.wrapped.SaveChanges(raw_material.wrapped if raw_material else None)
