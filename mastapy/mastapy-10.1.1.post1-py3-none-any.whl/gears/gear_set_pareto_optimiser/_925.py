'''_925.py

MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase
'''


from typing import Iterable

from mastapy.math_utility.optimisation import _945
from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_MICRO_GEOMETRY_GEAR_SET_DUTY_CYCLE_DESIGN_SPACE_SEARCH_STRATEGY_DATABASE = python_net_import('SMT.MastaAPI.Gears.GearSetParetoOptimiser', 'MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase',)


class MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase(_1.APIBase):
    '''MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase

    This is a mastapy class.
    '''

    TYPE = _MICRO_GEOMETRY_GEAR_SET_DUTY_CYCLE_DESIGN_SPACE_SEARCH_STRATEGY_DATABASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def item(self) -> '_945.ParetoOptimisationStrategy':
        '''ParetoOptimisationStrategy: 'Item' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_945.ParetoOptimisationStrategy)(self.wrapped.Item) if self.wrapped.Item else None

    def create(self, name: 'str') -> '_945.ParetoOptimisationStrategy':
        ''' 'Create' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.math_utility.optimisation.ParetoOptimisationStrategy
        '''

        name = str(name)
        method_result = self.wrapped.Create(name if name else None)
        return constructor.new(_945.ParetoOptimisationStrategy)(method_result) if method_result else None

    def can_be_removed(self, pareto_optimisation_strategy: '_945.ParetoOptimisationStrategy') -> 'bool':
        ''' 'CanBeRemoved' is the original name of this method.

        Args:
            pareto_optimisation_strategy (mastapy.math_utility.optimisation.ParetoOptimisationStrategy)

        Returns:
            bool
        '''

        method_result = self.wrapped.CanBeRemoved(pareto_optimisation_strategy.wrapped if pareto_optimisation_strategy else None)
        return method_result

    def rename(self, pareto_optimisation_strategy: '_945.ParetoOptimisationStrategy', new_name: 'str') -> 'bool':
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

    def remove(self, pareto_optimisation_strategy: '_945.ParetoOptimisationStrategy'):
        ''' 'Remove' is the original name of this method.

        Args:
            pareto_optimisation_strategy (mastapy.math_utility.optimisation.ParetoOptimisationStrategy)
        '''

        self.wrapped.Remove(pareto_optimisation_strategy.wrapped if pareto_optimisation_strategy else None)

    def get_all_items(self) -> 'Iterable[_945.ParetoOptimisationStrategy]':
        ''' 'GetAllItems' is the original name of this method.

        Returns:
            Iterable[mastapy.math_utility.optimisation.ParetoOptimisationStrategy]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.GetAllItems(), constructor.new(_945.ParetoOptimisationStrategy))

    def save_changes(self, pareto_optimisation_strategy: '_945.ParetoOptimisationStrategy'):
        ''' 'SaveChanges' is the original name of this method.

        Args:
            pareto_optimisation_strategy (mastapy.math_utility.optimisation.ParetoOptimisationStrategy)
        '''

        self.wrapped.SaveChanges(pareto_optimisation_strategy.wrapped if pareto_optimisation_strategy else None)
