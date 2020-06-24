'''_821.py

ManufacturingMachineDatabase
'''


from typing import Iterable

from mastapy.gears.manufacturing.bevel import _820
from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_MANUFACTURING_MACHINE_DATABASE = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'ManufacturingMachineDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('ManufacturingMachineDatabase',)


class ManufacturingMachineDatabase(_1.APIBase):
    '''ManufacturingMachineDatabase

    This is a mastapy class.
    '''

    TYPE = _MANUFACTURING_MACHINE_DATABASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ManufacturingMachineDatabase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def item(self) -> '_820.ManufacturingMachine':
        '''ManufacturingMachine: 'Item' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.ManufacturingMachine)(self.wrapped.Item) if self.wrapped.Item else None

    def create(self, name: 'str') -> '_820.ManufacturingMachine':
        ''' 'Create' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.gears.manufacturing.bevel.ManufacturingMachine
        '''

        name = str(name)
        method_result = self.wrapped.Create(name if name else None)
        return constructor.new(_820.ManufacturingMachine)(method_result) if method_result else None

    def can_be_removed(self, manufacturing_machine: '_820.ManufacturingMachine') -> 'bool':
        ''' 'CanBeRemoved' is the original name of this method.

        Args:
            manufacturing_machine (mastapy.gears.manufacturing.bevel.ManufacturingMachine)

        Returns:
            bool
        '''

        method_result = self.wrapped.CanBeRemoved(manufacturing_machine.wrapped if manufacturing_machine else None)
        return method_result

    def rename(self, manufacturing_machine: '_820.ManufacturingMachine', new_name: 'str') -> 'bool':
        ''' 'Rename' is the original name of this method.

        Args:
            manufacturing_machine (mastapy.gears.manufacturing.bevel.ManufacturingMachine)
            new_name (str)

        Returns:
            bool
        '''

        new_name = str(new_name)
        method_result = self.wrapped.Rename(manufacturing_machine.wrapped if manufacturing_machine else None, new_name if new_name else None)
        return method_result

    def remove(self, manufacturing_machine: '_820.ManufacturingMachine'):
        ''' 'Remove' is the original name of this method.

        Args:
            manufacturing_machine (mastapy.gears.manufacturing.bevel.ManufacturingMachine)
        '''

        self.wrapped.Remove(manufacturing_machine.wrapped if manufacturing_machine else None)

    def get_all_items(self) -> 'Iterable[_820.ManufacturingMachine]':
        ''' 'GetAllItems' is the original name of this method.

        Returns:
            Iterable[mastapy.gears.manufacturing.bevel.ManufacturingMachine]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.GetAllItems(), constructor.new(_820.ManufacturingMachine))

    def save_changes(self, manufacturing_machine: '_820.ManufacturingMachine'):
        ''' 'SaveChanges' is the original name of this method.

        Args:
            manufacturing_machine (mastapy.gears.manufacturing.bevel.ManufacturingMachine)
        '''

        self.wrapped.SaveChanges(manufacturing_machine.wrapped if manufacturing_machine else None)
