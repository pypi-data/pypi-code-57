'''_1752.py

OptimizationStrategyDatabase
'''


from typing import Iterable

from mastapy.system_model.optimization import _1744
from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_OPTIMIZATION_STRATEGY_DATABASE = python_net_import('SMT.MastaAPI.SystemModel.Optimization', 'OptimizationStrategyDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('OptimizationStrategyDatabase',)


class OptimizationStrategyDatabase(_1.APIBase):
    '''OptimizationStrategyDatabase

    This is a mastapy class.
    '''

    TYPE = _OPTIMIZATION_STRATEGY_DATABASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'OptimizationStrategyDatabase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def item(self) -> '_1744.CylindricalGearOptimisationStrategy':
        '''CylindricalGearOptimisationStrategy: 'Item' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1744.CylindricalGearOptimisationStrategy)(self.wrapped.Item) if self.wrapped.Item else None

    def create(self, name: 'str') -> '_1744.CylindricalGearOptimisationStrategy':
        ''' 'Create' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.optimization.CylindricalGearOptimisationStrategy
        '''

        name = str(name)
        method_result = self.wrapped.Create(name if name else None)
        return constructor.new(_1744.CylindricalGearOptimisationStrategy)(method_result) if method_result else None

    def can_be_removed(self, cylindrical_gear_optimisation_strategy: '_1744.CylindricalGearOptimisationStrategy') -> 'bool':
        ''' 'CanBeRemoved' is the original name of this method.

        Args:
            cylindrical_gear_optimisation_strategy (mastapy.system_model.optimization.CylindricalGearOptimisationStrategy)

        Returns:
            bool
        '''

        method_result = self.wrapped.CanBeRemoved(cylindrical_gear_optimisation_strategy.wrapped if cylindrical_gear_optimisation_strategy else None)
        return method_result

    def rename(self, cylindrical_gear_optimisation_strategy: '_1744.CylindricalGearOptimisationStrategy', new_name: 'str') -> 'bool':
        ''' 'Rename' is the original name of this method.

        Args:
            cylindrical_gear_optimisation_strategy (mastapy.system_model.optimization.CylindricalGearOptimisationStrategy)
            new_name (str)

        Returns:
            bool
        '''

        new_name = str(new_name)
        method_result = self.wrapped.Rename(cylindrical_gear_optimisation_strategy.wrapped if cylindrical_gear_optimisation_strategy else None, new_name if new_name else None)
        return method_result

    def remove(self, cylindrical_gear_optimisation_strategy: '_1744.CylindricalGearOptimisationStrategy'):
        ''' 'Remove' is the original name of this method.

        Args:
            cylindrical_gear_optimisation_strategy (mastapy.system_model.optimization.CylindricalGearOptimisationStrategy)
        '''

        self.wrapped.Remove(cylindrical_gear_optimisation_strategy.wrapped if cylindrical_gear_optimisation_strategy else None)

    def get_all_items(self) -> 'Iterable[_1744.CylindricalGearOptimisationStrategy]':
        ''' 'GetAllItems' is the original name of this method.

        Returns:
            Iterable[mastapy.system_model.optimization.CylindricalGearOptimisationStrategy]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.GetAllItems(), constructor.new(_1744.CylindricalGearOptimisationStrategy))

    def save_changes(self, cylindrical_gear_optimisation_strategy: '_1744.CylindricalGearOptimisationStrategy'):
        ''' 'SaveChanges' is the original name of this method.

        Args:
            cylindrical_gear_optimisation_strategy (mastapy.system_model.optimization.CylindricalGearOptimisationStrategy)
        '''

        self.wrapped.SaveChanges(cylindrical_gear_optimisation_strategy.wrapped if cylindrical_gear_optimisation_strategy else None)
