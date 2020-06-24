'''_600.py

ISOTR1417912001CoefficientOfFrictionConstantsDatabase
'''


from typing import Iterable

from mastapy.gears.materials import _599
from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_ISOTR1417912001_COEFFICIENT_OF_FRICTION_CONSTANTS_DATABASE = python_net_import('SMT.MastaAPI.Gears.Materials', 'ISOTR1417912001CoefficientOfFrictionConstantsDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('ISOTR1417912001CoefficientOfFrictionConstantsDatabase',)


class ISOTR1417912001CoefficientOfFrictionConstantsDatabase(_1.APIBase):
    '''ISOTR1417912001CoefficientOfFrictionConstantsDatabase

    This is a mastapy class.
    '''

    TYPE = _ISOTR1417912001_COEFFICIENT_OF_FRICTION_CONSTANTS_DATABASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ISOTR1417912001CoefficientOfFrictionConstantsDatabase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def item(self) -> '_599.ISOTR1417912001CoefficientOfFrictionConstants':
        '''ISOTR1417912001CoefficientOfFrictionConstants: 'Item' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_599.ISOTR1417912001CoefficientOfFrictionConstants)(self.wrapped.Item) if self.wrapped.Item else None

    def create(self, name: 'str') -> '_599.ISOTR1417912001CoefficientOfFrictionConstants':
        ''' 'Create' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.gears.materials.ISOTR1417912001CoefficientOfFrictionConstants
        '''

        name = str(name)
        method_result = self.wrapped.Create(name if name else None)
        return constructor.new(_599.ISOTR1417912001CoefficientOfFrictionConstants)(method_result) if method_result else None

    def can_be_removed(self, isotr1417912001_coefficient_of_friction_constants: '_599.ISOTR1417912001CoefficientOfFrictionConstants') -> 'bool':
        ''' 'CanBeRemoved' is the original name of this method.

        Args:
            isotr1417912001_coefficient_of_friction_constants (mastapy.gears.materials.ISOTR1417912001CoefficientOfFrictionConstants)

        Returns:
            bool
        '''

        method_result = self.wrapped.CanBeRemoved(isotr1417912001_coefficient_of_friction_constants.wrapped if isotr1417912001_coefficient_of_friction_constants else None)
        return method_result

    def rename(self, isotr1417912001_coefficient_of_friction_constants: '_599.ISOTR1417912001CoefficientOfFrictionConstants', new_name: 'str') -> 'bool':
        ''' 'Rename' is the original name of this method.

        Args:
            isotr1417912001_coefficient_of_friction_constants (mastapy.gears.materials.ISOTR1417912001CoefficientOfFrictionConstants)
            new_name (str)

        Returns:
            bool
        '''

        new_name = str(new_name)
        method_result = self.wrapped.Rename(isotr1417912001_coefficient_of_friction_constants.wrapped if isotr1417912001_coefficient_of_friction_constants else None, new_name if new_name else None)
        return method_result

    def remove(self, isotr1417912001_coefficient_of_friction_constants: '_599.ISOTR1417912001CoefficientOfFrictionConstants'):
        ''' 'Remove' is the original name of this method.

        Args:
            isotr1417912001_coefficient_of_friction_constants (mastapy.gears.materials.ISOTR1417912001CoefficientOfFrictionConstants)
        '''

        self.wrapped.Remove(isotr1417912001_coefficient_of_friction_constants.wrapped if isotr1417912001_coefficient_of_friction_constants else None)

    def get_all_items(self) -> 'Iterable[_599.ISOTR1417912001CoefficientOfFrictionConstants]':
        ''' 'GetAllItems' is the original name of this method.

        Returns:
            Iterable[mastapy.gears.materials.ISOTR1417912001CoefficientOfFrictionConstants]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.GetAllItems(), constructor.new(_599.ISOTR1417912001CoefficientOfFrictionConstants))

    def save_changes(self, isotr1417912001_coefficient_of_friction_constants: '_599.ISOTR1417912001CoefficientOfFrictionConstants'):
        ''' 'SaveChanges' is the original name of this method.

        Args:
            isotr1417912001_coefficient_of_friction_constants (mastapy.gears.materials.ISOTR1417912001CoefficientOfFrictionConstants)
        '''

        self.wrapped.SaveChanges(isotr1417912001_coefficient_of_friction_constants.wrapped if isotr1417912001_coefficient_of_friction_constants else None)
