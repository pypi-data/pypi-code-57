'''_1743.py

ConicalGearOptimizationStrategyDatabase
'''


from typing import Iterable

from mastapy.system_model.optimization import _1741
from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_OPTIMIZATION_STRATEGY_DATABASE = python_net_import('SMT.MastaAPI.SystemModel.Optimization', 'ConicalGearOptimizationStrategyDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearOptimizationStrategyDatabase',)


class ConicalGearOptimizationStrategyDatabase(_1.APIBase):
    '''ConicalGearOptimizationStrategyDatabase

    This is a mastapy class.
    '''

    TYPE = _CONICAL_GEAR_OPTIMIZATION_STRATEGY_DATABASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalGearOptimizationStrategyDatabase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def item(self) -> '_1741.ConicalGearOptimisationStrategy':
        '''ConicalGearOptimisationStrategy: 'Item' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1741.ConicalGearOptimisationStrategy)(self.wrapped.Item) if self.wrapped.Item else None

    def create(self, name: 'str') -> '_1741.ConicalGearOptimisationStrategy':
        ''' 'Create' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.optimization.ConicalGearOptimisationStrategy
        '''

        name = str(name)
        method_result = self.wrapped.Create(name if name else None)
        return constructor.new(_1741.ConicalGearOptimisationStrategy)(method_result) if method_result else None

    def can_be_removed(self, conical_gear_optimisation_strategy: '_1741.ConicalGearOptimisationStrategy') -> 'bool':
        ''' 'CanBeRemoved' is the original name of this method.

        Args:
            conical_gear_optimisation_strategy (mastapy.system_model.optimization.ConicalGearOptimisationStrategy)

        Returns:
            bool
        '''

        method_result = self.wrapped.CanBeRemoved(conical_gear_optimisation_strategy.wrapped if conical_gear_optimisation_strategy else None)
        return method_result

    def rename(self, conical_gear_optimisation_strategy: '_1741.ConicalGearOptimisationStrategy', new_name: 'str') -> 'bool':
        ''' 'Rename' is the original name of this method.

        Args:
            conical_gear_optimisation_strategy (mastapy.system_model.optimization.ConicalGearOptimisationStrategy)
            new_name (str)

        Returns:
            bool
        '''

        new_name = str(new_name)
        method_result = self.wrapped.Rename(conical_gear_optimisation_strategy.wrapped if conical_gear_optimisation_strategy else None, new_name if new_name else None)
        return method_result

    def remove(self, conical_gear_optimisation_strategy: '_1741.ConicalGearOptimisationStrategy'):
        ''' 'Remove' is the original name of this method.

        Args:
            conical_gear_optimisation_strategy (mastapy.system_model.optimization.ConicalGearOptimisationStrategy)
        '''

        self.wrapped.Remove(conical_gear_optimisation_strategy.wrapped if conical_gear_optimisation_strategy else None)

    def get_all_items(self) -> 'Iterable[_1741.ConicalGearOptimisationStrategy]':
        ''' 'GetAllItems' is the original name of this method.

        Returns:
            Iterable[mastapy.system_model.optimization.ConicalGearOptimisationStrategy]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.GetAllItems(), constructor.new(_1741.ConicalGearOptimisationStrategy))

    def save_changes(self, conical_gear_optimisation_strategy: '_1741.ConicalGearOptimisationStrategy'):
        ''' 'SaveChanges' is the original name of this method.

        Args:
            conical_gear_optimisation_strategy (mastapy.system_model.optimization.ConicalGearOptimisationStrategy)
        '''

        self.wrapped.SaveChanges(conical_gear_optimisation_strategy.wrapped if conical_gear_optimisation_strategy else None)
