'''_747.py

CylindricalFormedWheelGrinderDatabase
'''


from typing import Iterable

from mastapy.gears.manufacturing.cylindrical.cutters import _749
from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_FORMED_WHEEL_GRINDER_DATABASE = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters', 'CylindricalFormedWheelGrinderDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalFormedWheelGrinderDatabase',)


class CylindricalFormedWheelGrinderDatabase(_1.APIBase):
    '''CylindricalFormedWheelGrinderDatabase

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_FORMED_WHEEL_GRINDER_DATABASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalFormedWheelGrinderDatabase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def item(self) -> '_749.CylindricalGearFormGrindingWheel':
        '''CylindricalGearFormGrindingWheel: 'Item' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_749.CylindricalGearFormGrindingWheel)(self.wrapped.Item) if self.wrapped.Item else None

    def create(self, name: 'str') -> '_749.CylindricalGearFormGrindingWheel':
        ''' 'Create' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearFormGrindingWheel
        '''

        name = str(name)
        method_result = self.wrapped.Create(name if name else None)
        return constructor.new(_749.CylindricalGearFormGrindingWheel)(method_result) if method_result else None

    def can_be_removed(self, cylindrical_gear_form_grinding_wheel: '_749.CylindricalGearFormGrindingWheel') -> 'bool':
        ''' 'CanBeRemoved' is the original name of this method.

        Args:
            cylindrical_gear_form_grinding_wheel (mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearFormGrindingWheel)

        Returns:
            bool
        '''

        method_result = self.wrapped.CanBeRemoved(cylindrical_gear_form_grinding_wheel.wrapped if cylindrical_gear_form_grinding_wheel else None)
        return method_result

    def rename(self, cylindrical_gear_form_grinding_wheel: '_749.CylindricalGearFormGrindingWheel', new_name: 'str') -> 'bool':
        ''' 'Rename' is the original name of this method.

        Args:
            cylindrical_gear_form_grinding_wheel (mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearFormGrindingWheel)
            new_name (str)

        Returns:
            bool
        '''

        new_name = str(new_name)
        method_result = self.wrapped.Rename(cylindrical_gear_form_grinding_wheel.wrapped if cylindrical_gear_form_grinding_wheel else None, new_name if new_name else None)
        return method_result

    def remove(self, cylindrical_gear_form_grinding_wheel: '_749.CylindricalGearFormGrindingWheel'):
        ''' 'Remove' is the original name of this method.

        Args:
            cylindrical_gear_form_grinding_wheel (mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearFormGrindingWheel)
        '''

        self.wrapped.Remove(cylindrical_gear_form_grinding_wheel.wrapped if cylindrical_gear_form_grinding_wheel else None)

    def get_all_items(self) -> 'Iterable[_749.CylindricalGearFormGrindingWheel]':
        ''' 'GetAllItems' is the original name of this method.

        Returns:
            Iterable[mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearFormGrindingWheel]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.GetAllItems(), constructor.new(_749.CylindricalGearFormGrindingWheel))

    def save_changes(self, cylindrical_gear_form_grinding_wheel: '_749.CylindricalGearFormGrindingWheel'):
        ''' 'SaveChanges' is the original name of this method.

        Args:
            cylindrical_gear_form_grinding_wheel (mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearFormGrindingWheel)
        '''

        self.wrapped.SaveChanges(cylindrical_gear_form_grinding_wheel.wrapped if cylindrical_gear_form_grinding_wheel else None)
