'''_2023.py

SuperchargerRotorSetDatabase
'''


from typing import Iterable

from mastapy.system_model.part_model.gears.supercharger_rotor_set import _2022
from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_SUPERCHARGER_ROTOR_SET_DATABASE = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears.SuperchargerRotorSet', 'SuperchargerRotorSetDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('SuperchargerRotorSetDatabase',)


class SuperchargerRotorSetDatabase(_1.APIBase):
    '''SuperchargerRotorSetDatabase

    This is a mastapy class.
    '''

    TYPE = _SUPERCHARGER_ROTOR_SET_DATABASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SuperchargerRotorSetDatabase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def item(self) -> '_2022.SuperchargerRotorSet':
        '''SuperchargerRotorSet: 'Item' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2022.SuperchargerRotorSet)(self.wrapped.Item) if self.wrapped.Item else None

    def create(self, name: 'str') -> '_2022.SuperchargerRotorSet':
        ''' 'Create' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.supercharger_rotor_set.SuperchargerRotorSet
        '''

        name = str(name)
        method_result = self.wrapped.Create(name if name else None)
        return constructor.new(_2022.SuperchargerRotorSet)(method_result) if method_result else None

    def can_be_removed(self, supercharger_rotor_set: '_2022.SuperchargerRotorSet') -> 'bool':
        ''' 'CanBeRemoved' is the original name of this method.

        Args:
            supercharger_rotor_set (mastapy.system_model.part_model.gears.supercharger_rotor_set.SuperchargerRotorSet)

        Returns:
            bool
        '''

        method_result = self.wrapped.CanBeRemoved(supercharger_rotor_set.wrapped if supercharger_rotor_set else None)
        return method_result

    def rename(self, supercharger_rotor_set: '_2022.SuperchargerRotorSet', new_name: 'str') -> 'bool':
        ''' 'Rename' is the original name of this method.

        Args:
            supercharger_rotor_set (mastapy.system_model.part_model.gears.supercharger_rotor_set.SuperchargerRotorSet)
            new_name (str)

        Returns:
            bool
        '''

        new_name = str(new_name)
        method_result = self.wrapped.Rename(supercharger_rotor_set.wrapped if supercharger_rotor_set else None, new_name if new_name else None)
        return method_result

    def remove(self, supercharger_rotor_set: '_2022.SuperchargerRotorSet'):
        ''' 'Remove' is the original name of this method.

        Args:
            supercharger_rotor_set (mastapy.system_model.part_model.gears.supercharger_rotor_set.SuperchargerRotorSet)
        '''

        self.wrapped.Remove(supercharger_rotor_set.wrapped if supercharger_rotor_set else None)

    def get_all_items(self) -> 'Iterable[_2022.SuperchargerRotorSet]':
        ''' 'GetAllItems' is the original name of this method.

        Returns:
            Iterable[mastapy.system_model.part_model.gears.supercharger_rotor_set.SuperchargerRotorSet]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.GetAllItems(), constructor.new(_2022.SuperchargerRotorSet))

    def save_changes(self, supercharger_rotor_set: '_2022.SuperchargerRotorSet'):
        ''' 'SaveChanges' is the original name of this method.

        Args:
            supercharger_rotor_set (mastapy.system_model.part_model.gears.supercharger_rotor_set.SuperchargerRotorSet)
        '''

        self.wrapped.SaveChanges(supercharger_rotor_set.wrapped if supercharger_rotor_set else None)
