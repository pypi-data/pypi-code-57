'''_981.py

CylindricalGearDesignConstraintsDatabase
'''


from typing import Iterable

from mastapy.gears.gear_designs.cylindrical import _980
from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_DESIGN_CONSTRAINTS_DATABASE = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'CylindricalGearDesignConstraintsDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearDesignConstraintsDatabase',)


class CylindricalGearDesignConstraintsDatabase(_1.APIBase):
    '''CylindricalGearDesignConstraintsDatabase

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_DESIGN_CONSTRAINTS_DATABASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearDesignConstraintsDatabase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def item(self) -> '_980.CylindricalGearDesignConstraints':
        '''CylindricalGearDesignConstraints: 'Item' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_980.CylindricalGearDesignConstraints)(self.wrapped.Item) if self.wrapped.Item else None

    def create(self, name: 'str') -> '_980.CylindricalGearDesignConstraints':
        ''' 'Create' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.gears.gear_designs.cylindrical.CylindricalGearDesignConstraints
        '''

        name = str(name)
        method_result = self.wrapped.Create(name if name else None)
        return constructor.new(_980.CylindricalGearDesignConstraints)(method_result) if method_result else None

    def can_be_removed(self, cylindrical_gear_design_constraints: '_980.CylindricalGearDesignConstraints') -> 'bool':
        ''' 'CanBeRemoved' is the original name of this method.

        Args:
            cylindrical_gear_design_constraints (mastapy.gears.gear_designs.cylindrical.CylindricalGearDesignConstraints)

        Returns:
            bool
        '''

        method_result = self.wrapped.CanBeRemoved(cylindrical_gear_design_constraints.wrapped if cylindrical_gear_design_constraints else None)
        return method_result

    def rename(self, cylindrical_gear_design_constraints: '_980.CylindricalGearDesignConstraints', new_name: 'str') -> 'bool':
        ''' 'Rename' is the original name of this method.

        Args:
            cylindrical_gear_design_constraints (mastapy.gears.gear_designs.cylindrical.CylindricalGearDesignConstraints)
            new_name (str)

        Returns:
            bool
        '''

        new_name = str(new_name)
        method_result = self.wrapped.Rename(cylindrical_gear_design_constraints.wrapped if cylindrical_gear_design_constraints else None, new_name if new_name else None)
        return method_result

    def remove(self, cylindrical_gear_design_constraints: '_980.CylindricalGearDesignConstraints'):
        ''' 'Remove' is the original name of this method.

        Args:
            cylindrical_gear_design_constraints (mastapy.gears.gear_designs.cylindrical.CylindricalGearDesignConstraints)
        '''

        self.wrapped.Remove(cylindrical_gear_design_constraints.wrapped if cylindrical_gear_design_constraints else None)

    def get_all_items(self) -> 'Iterable[_980.CylindricalGearDesignConstraints]':
        ''' 'GetAllItems' is the original name of this method.

        Returns:
            Iterable[mastapy.gears.gear_designs.cylindrical.CylindricalGearDesignConstraints]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.GetAllItems(), constructor.new(_980.CylindricalGearDesignConstraints))

    def save_changes(self, cylindrical_gear_design_constraints: '_980.CylindricalGearDesignConstraints'):
        ''' 'SaveChanges' is the original name of this method.

        Args:
            cylindrical_gear_design_constraints (mastapy.gears.gear_designs.cylindrical.CylindricalGearDesignConstraints)
        '''

        self.wrapped.SaveChanges(cylindrical_gear_design_constraints.wrapped if cylindrical_gear_design_constraints else None)
