'''_1077.py

ParetoOptimisationStrategyBars
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_PARETO_OPTIMISATION_STRATEGY_BARS = python_net_import('SMT.MastaAPI.MathUtility.Optimisation', 'ParetoOptimisationStrategyBars')


__docformat__ = 'restructuredtext en'
__all__ = ('ParetoOptimisationStrategyBars',)


class ParetoOptimisationStrategyBars(_1.APIBase):
    '''ParetoOptimisationStrategyBars

    This is a mastapy class.
    '''

    TYPE = _PARETO_OPTIMISATION_STRATEGY_BARS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ParetoOptimisationStrategyBars.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def remove_bar(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'RemoveBar' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RemoveBar
