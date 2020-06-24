'''_51.py

ShaftMaterialDatabase
'''


from typing import Iterable

from mastapy.shafts import _50
from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_SHAFT_MATERIAL_DATABASE = python_net_import('SMT.MastaAPI.Shafts', 'ShaftMaterialDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftMaterialDatabase',)


class ShaftMaterialDatabase(_1.APIBase):
    '''ShaftMaterialDatabase

    This is a mastapy class.
    '''

    TYPE = _SHAFT_MATERIAL_DATABASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftMaterialDatabase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def item(self) -> '_50.ShaftMaterial':
        '''ShaftMaterial: 'Item' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_50.ShaftMaterial)(self.wrapped.Item) if self.wrapped.Item else None

    def create(self, name: 'str') -> '_50.ShaftMaterial':
        ''' 'Create' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.shafts.ShaftMaterial
        '''

        name = str(name)
        method_result = self.wrapped.Create(name if name else None)
        return constructor.new(_50.ShaftMaterial)(method_result) if method_result else None

    def can_be_removed(self, shaft_material: '_50.ShaftMaterial') -> 'bool':
        ''' 'CanBeRemoved' is the original name of this method.

        Args:
            shaft_material (mastapy.shafts.ShaftMaterial)

        Returns:
            bool
        '''

        method_result = self.wrapped.CanBeRemoved(shaft_material.wrapped if shaft_material else None)
        return method_result

    def rename(self, shaft_material: '_50.ShaftMaterial', new_name: 'str') -> 'bool':
        ''' 'Rename' is the original name of this method.

        Args:
            shaft_material (mastapy.shafts.ShaftMaterial)
            new_name (str)

        Returns:
            bool
        '''

        new_name = str(new_name)
        method_result = self.wrapped.Rename(shaft_material.wrapped if shaft_material else None, new_name if new_name else None)
        return method_result

    def remove(self, shaft_material: '_50.ShaftMaterial'):
        ''' 'Remove' is the original name of this method.

        Args:
            shaft_material (mastapy.shafts.ShaftMaterial)
        '''

        self.wrapped.Remove(shaft_material.wrapped if shaft_material else None)

    def get_all_items(self) -> 'Iterable[_50.ShaftMaterial]':
        ''' 'GetAllItems' is the original name of this method.

        Returns:
            Iterable[mastapy.shafts.ShaftMaterial]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.GetAllItems(), constructor.new(_50.ShaftMaterial))

    def save_changes(self, shaft_material: '_50.ShaftMaterial'):
        ''' 'SaveChanges' is the original name of this method.

        Args:
            shaft_material (mastapy.shafts.ShaftMaterial)
        '''

        self.wrapped.SaveChanges(shaft_material.wrapped if shaft_material else None)
