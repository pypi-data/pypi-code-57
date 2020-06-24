'''_615.py

CylindricalHobDatabase
'''


from typing import Iterable

from mastapy.gears.manufacturing.cylindrical.cutters import _663
from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_HOB_DATABASE = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical', 'CylindricalHobDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalHobDatabase',)


class CylindricalHobDatabase(_1.APIBase):
    '''CylindricalHobDatabase

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_HOB_DATABASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalHobDatabase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def item(self) -> '_663.CylindricalGearHobDesign':
        '''CylindricalGearHobDesign: 'Item' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_663.CylindricalGearHobDesign)(self.wrapped.Item) if self.wrapped.Item else None

    def create(self, name: 'str') -> '_663.CylindricalGearHobDesign':
        ''' 'Create' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearHobDesign
        '''

        name = str(name)
        method_result = self.wrapped.Create(name if name else None)
        return constructor.new(_663.CylindricalGearHobDesign)(method_result) if method_result else None

    def can_be_removed(self, cylindrical_gear_hob_design: '_663.CylindricalGearHobDesign') -> 'bool':
        ''' 'CanBeRemoved' is the original name of this method.

        Args:
            cylindrical_gear_hob_design (mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearHobDesign)

        Returns:
            bool
        '''

        method_result = self.wrapped.CanBeRemoved(cylindrical_gear_hob_design.wrapped if cylindrical_gear_hob_design else None)
        return method_result

    def rename(self, cylindrical_gear_hob_design: '_663.CylindricalGearHobDesign', new_name: 'str') -> 'bool':
        ''' 'Rename' is the original name of this method.

        Args:
            cylindrical_gear_hob_design (mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearHobDesign)
            new_name (str)

        Returns:
            bool
        '''

        new_name = str(new_name)
        method_result = self.wrapped.Rename(cylindrical_gear_hob_design.wrapped if cylindrical_gear_hob_design else None, new_name if new_name else None)
        return method_result

    def remove(self, cylindrical_gear_hob_design: '_663.CylindricalGearHobDesign'):
        ''' 'Remove' is the original name of this method.

        Args:
            cylindrical_gear_hob_design (mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearHobDesign)
        '''

        self.wrapped.Remove(cylindrical_gear_hob_design.wrapped if cylindrical_gear_hob_design else None)

    def get_all_items(self) -> 'Iterable[_663.CylindricalGearHobDesign]':
        ''' 'GetAllItems' is the original name of this method.

        Returns:
            Iterable[mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearHobDesign]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.GetAllItems(), constructor.new(_663.CylindricalGearHobDesign))

    def save_changes(self, cylindrical_gear_hob_design: '_663.CylindricalGearHobDesign'):
        ''' 'SaveChanges' is the original name of this method.

        Args:
            cylindrical_gear_hob_design (mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearHobDesign)
        '''

        self.wrapped.SaveChanges(cylindrical_gear_hob_design.wrapped if cylindrical_gear_hob_design else None)
