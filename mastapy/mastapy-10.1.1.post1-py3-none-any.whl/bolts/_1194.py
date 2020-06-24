'''_1194.py

BoltMaterialDatabase
'''


from typing import Iterable

from mastapy.bolts import _1193
from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_BOLT_MATERIAL_DATABASE = python_net_import('SMT.MastaAPI.Bolts', 'BoltMaterialDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltMaterialDatabase',)


class BoltMaterialDatabase(_1.APIBase):
    '''BoltMaterialDatabase

    This is a mastapy class.
    '''

    TYPE = _BOLT_MATERIAL_DATABASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltMaterialDatabase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def item(self) -> '_1193.BoltMaterial':
        '''BoltMaterial: 'Item' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1193.BoltMaterial)(self.wrapped.Item) if self.wrapped.Item else None

    def create(self, name: 'str') -> '_1193.BoltMaterial':
        ''' 'Create' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.bolts.BoltMaterial
        '''

        name = str(name)
        method_result = self.wrapped.Create(name if name else None)
        return constructor.new(_1193.BoltMaterial)(method_result) if method_result else None

    def can_be_removed(self, bolt_material: '_1193.BoltMaterial') -> 'bool':
        ''' 'CanBeRemoved' is the original name of this method.

        Args:
            bolt_material (mastapy.bolts.BoltMaterial)

        Returns:
            bool
        '''

        method_result = self.wrapped.CanBeRemoved(bolt_material.wrapped if bolt_material else None)
        return method_result

    def rename(self, bolt_material: '_1193.BoltMaterial', new_name: 'str') -> 'bool':
        ''' 'Rename' is the original name of this method.

        Args:
            bolt_material (mastapy.bolts.BoltMaterial)
            new_name (str)

        Returns:
            bool
        '''

        new_name = str(new_name)
        method_result = self.wrapped.Rename(bolt_material.wrapped if bolt_material else None, new_name if new_name else None)
        return method_result

    def remove(self, bolt_material: '_1193.BoltMaterial'):
        ''' 'Remove' is the original name of this method.

        Args:
            bolt_material (mastapy.bolts.BoltMaterial)
        '''

        self.wrapped.Remove(bolt_material.wrapped if bolt_material else None)

    def get_all_items(self) -> 'Iterable[_1193.BoltMaterial]':
        ''' 'GetAllItems' is the original name of this method.

        Returns:
            Iterable[mastapy.bolts.BoltMaterial]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.GetAllItems(), constructor.new(_1193.BoltMaterial))

    def save_changes(self, bolt_material: '_1193.BoltMaterial'):
        ''' 'SaveChanges' is the original name of this method.

        Args:
            bolt_material (mastapy.bolts.BoltMaterial)
        '''

        self.wrapped.SaveChanges(bolt_material.wrapped if bolt_material else None)
