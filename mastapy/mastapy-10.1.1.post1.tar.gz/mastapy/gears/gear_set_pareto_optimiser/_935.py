'''_935.py

ParetoHypoidGearSetOptimisationStrategyDatabase
'''


from typing import Iterable

from mastapy.math_utility.optimisation import _1007
from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_PARETO_HYPOID_GEAR_SET_OPTIMISATION_STRATEGY_DATABASE = python_net_import('SMT.MastaAPI.Gears.GearSetParetoOptimiser', 'ParetoHypoidGearSetOptimisationStrategyDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('ParetoHypoidGearSetOptimisationStrategyDatabase',)


class ParetoHypoidGearSetOptimisationStrategyDatabase(_1.APIBase):
    '''ParetoHypoidGearSetOptimisationStrategyDatabase

    This is a mastapy class.
    '''

    TYPE = _PARETO_HYPOID_GEAR_SET_OPTIMISATION_STRATEGY_DATABASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ParetoHypoidGearSetOptimisationStrategyDatabase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def item(self) -> '_1007.ParetoOptimisationStrategy':
        '''ParetoOptimisationStrategy: 'Item' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1007.ParetoOptimisationStrategy)(self.wrapped.Item) if self.wrapped.Item else None

    def create(self, name: 'str') -> '_1007.ParetoOptimisationStrategy':
        ''' 'Create' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.math_utility.optimisation.ParetoOptimisationStrategy
        '''

        name = str(name)
        method_result = self.wrapped.Create(name if name else None)
        return constructor.new(_1007.ParetoOptimisationStrategy)(method_result) if method_result else None

    def can_be_removed(self, pareto_optimisation_strategy: '_1007.ParetoOptimisationStrategy') -> 'bool':
        ''' 'CanBeRemoved' is the original name of this method.

        Args:
            pareto_optimisation_strategy (mastapy.math_utility.optimisation.ParetoOptimisationStrategy)

        Returns:
            bool
        '''

        method_result = self.wrapped.CanBeRemoved(pareto_optimisation_strategy.wrapped if pareto_optimisation_strategy else None)
        return method_result

    def rename(self, pareto_optimisation_strategy: '_1007.ParetoOptimisationStrategy', new_name: 'str') -> 'bool':
        ''' 'Rename' is the original name of this method.

        Args:
            pareto_optimisation_strategy (mastapy.math_utility.optimisation.ParetoOptimisationStrategy)
            new_name (str)

        Returns:
            bool
        '''

        new_name = str(new_name)
        method_result = self.wrapped.Rename(pareto_optimisation_strategy.wrapped if pareto_optimisation_strategy else None, new_name if new_name else None)
        return method_result

    def remove(self, pareto_optimisation_strategy: '_1007.ParetoOptimisationStrategy'):
        ''' 'Remove' is the original name of this method.

        Args:
            pareto_optimisation_strategy (mastapy.math_utility.optimisation.ParetoOptimisationStrategy)
        '''

        self.wrapped.Remove(pareto_optimisation_strategy.wrapped if pareto_optimisation_strategy else None)

    def get_all_items(self) -> 'Iterable[_1007.ParetoOptimisationStrategy]':
        ''' 'GetAllItems' is the original name of this method.

        Returns:
            Iterable[mastapy.math_utility.optimisation.ParetoOptimisationStrategy]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.GetAllItems(), constructor.new(_1007.ParetoOptimisationStrategy))

    def save_changes(self, pareto_optimisation_strategy: '_1007.ParetoOptimisationStrategy'):
        ''' 'SaveChanges' is the original name of this method.

        Args:
            pareto_optimisation_strategy (mastapy.math_utility.optimisation.ParetoOptimisationStrategy)
        '''

        self.wrapped.SaveChanges(pareto_optimisation_strategy.wrapped if pareto_optimisation_strategy else None)
