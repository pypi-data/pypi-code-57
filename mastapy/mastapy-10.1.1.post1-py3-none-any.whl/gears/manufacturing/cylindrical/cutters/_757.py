'''_757.py

CylindricalWormGrinderDatabase
'''


from typing import Iterable

from mastapy.gears.manufacturing.cylindrical.cutters import _750
from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_WORM_GRINDER_DATABASE = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters', 'CylindricalWormGrinderDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalWormGrinderDatabase',)


class CylindricalWormGrinderDatabase(_1.APIBase):
    '''CylindricalWormGrinderDatabase

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_WORM_GRINDER_DATABASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalWormGrinderDatabase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def item(self) -> '_750.CylindricalGearGrindingWorm':
        '''CylindricalGearGrindingWorm: 'Item' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_750.CylindricalGearGrindingWorm)(self.wrapped.Item) if self.wrapped.Item else None

    def create(self, name: 'str') -> '_750.CylindricalGearGrindingWorm':
        ''' 'Create' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearGrindingWorm
        '''

        name = str(name)
        method_result = self.wrapped.Create(name if name else None)
        return constructor.new(_750.CylindricalGearGrindingWorm)(method_result) if method_result else None

    def can_be_removed(self, cylindrical_gear_grinding_worm: '_750.CylindricalGearGrindingWorm') -> 'bool':
        ''' 'CanBeRemoved' is the original name of this method.

        Args:
            cylindrical_gear_grinding_worm (mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearGrindingWorm)

        Returns:
            bool
        '''

        method_result = self.wrapped.CanBeRemoved(cylindrical_gear_grinding_worm.wrapped if cylindrical_gear_grinding_worm else None)
        return method_result

    def rename(self, cylindrical_gear_grinding_worm: '_750.CylindricalGearGrindingWorm', new_name: 'str') -> 'bool':
        ''' 'Rename' is the original name of this method.

        Args:
            cylindrical_gear_grinding_worm (mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearGrindingWorm)
            new_name (str)

        Returns:
            bool
        '''

        new_name = str(new_name)
        method_result = self.wrapped.Rename(cylindrical_gear_grinding_worm.wrapped if cylindrical_gear_grinding_worm else None, new_name if new_name else None)
        return method_result

    def remove(self, cylindrical_gear_grinding_worm: '_750.CylindricalGearGrindingWorm'):
        ''' 'Remove' is the original name of this method.

        Args:
            cylindrical_gear_grinding_worm (mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearGrindingWorm)
        '''

        self.wrapped.Remove(cylindrical_gear_grinding_worm.wrapped if cylindrical_gear_grinding_worm else None)

    def get_all_items(self) -> 'Iterable[_750.CylindricalGearGrindingWorm]':
        ''' 'GetAllItems' is the original name of this method.

        Returns:
            Iterable[mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearGrindingWorm]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.GetAllItems(), constructor.new(_750.CylindricalGearGrindingWorm))

    def save_changes(self, cylindrical_gear_grinding_worm: '_750.CylindricalGearGrindingWorm'):
        ''' 'SaveChanges' is the original name of this method.

        Args:
            cylindrical_gear_grinding_worm (mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearGrindingWorm)
        '''

        self.wrapped.SaveChanges(cylindrical_gear_grinding_worm.wrapped if cylindrical_gear_grinding_worm else None)
