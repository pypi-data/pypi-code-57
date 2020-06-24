'''_238.py

ComponentMaterialDatabase
'''


from typing import Iterable

from mastapy.materials import _64
from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_COMPONENT_MATERIAL_DATABASE = python_net_import('SMT.MastaAPI.Materials', 'ComponentMaterialDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('ComponentMaterialDatabase',)


class ComponentMaterialDatabase(_1.APIBase):
    '''ComponentMaterialDatabase

    This is a mastapy class.
    '''

    TYPE = _COMPONENT_MATERIAL_DATABASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ComponentMaterialDatabase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def item(self) -> '_64.Material':
        '''Material: 'Item' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_64.Material)(self.wrapped.Item) if self.wrapped.Item else None

    def create(self, name: 'str') -> '_64.Material':
        ''' 'Create' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.materials.Material
        '''

        name = str(name)
        method_result = self.wrapped.Create(name if name else None)
        return constructor.new(_64.Material)(method_result) if method_result else None

    def can_be_removed(self, material: '_64.Material') -> 'bool':
        ''' 'CanBeRemoved' is the original name of this method.

        Args:
            material (mastapy.materials.Material)

        Returns:
            bool
        '''

        method_result = self.wrapped.CanBeRemoved(material.wrapped if material else None)
        return method_result

    def rename(self, material: '_64.Material', new_name: 'str') -> 'bool':
        ''' 'Rename' is the original name of this method.

        Args:
            material (mastapy.materials.Material)
            new_name (str)

        Returns:
            bool
        '''

        new_name = str(new_name)
        method_result = self.wrapped.Rename(material.wrapped if material else None, new_name if new_name else None)
        return method_result

    def remove(self, material: '_64.Material'):
        ''' 'Remove' is the original name of this method.

        Args:
            material (mastapy.materials.Material)
        '''

        self.wrapped.Remove(material.wrapped if material else None)

    def get_all_items(self) -> 'Iterable[_64.Material]':
        ''' 'GetAllItems' is the original name of this method.

        Returns:
            Iterable[mastapy.materials.Material]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.GetAllItems(), constructor.new(_64.Material))

    def save_changes(self, material: '_64.Material'):
        ''' 'SaveChanges' is the original name of this method.

        Args:
            material (mastapy.materials.Material)
        '''

        self.wrapped.SaveChanges(material.wrapped if material else None)
