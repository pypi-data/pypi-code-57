'''_1007.py

ParetoOptimisationStrategy
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.math_utility.optimisation import _1239, _1240, _1078
from mastapy.utility.databases import _89
from mastapy._internal.python_net import python_net_import

_PARETO_OPTIMISATION_STRATEGY = python_net_import('SMT.MastaAPI.MathUtility.Optimisation', 'ParetoOptimisationStrategy')


__docformat__ = 'restructuredtext en'
__all__ = ('ParetoOptimisationStrategy',)


class ParetoOptimisationStrategy(_89.NamedDatabaseItem):
    '''ParetoOptimisationStrategy

    This is a mastapy class.
    '''

    TYPE = _PARETO_OPTIMISATION_STRATEGY
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ParetoOptimisationStrategy.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def add_chart(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'AddChart' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AddChart

    @property
    def inputs(self) -> 'List[_1239.ParetoOptimisationInput]':
        '''List[ParetoOptimisationInput]: 'Inputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Inputs, constructor.new(_1239.ParetoOptimisationInput))
        return value

    @property
    def outputs(self) -> 'List[_1240.ParetoOptimisationOutput]':
        '''List[ParetoOptimisationOutput]: 'Outputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Outputs, constructor.new(_1240.ParetoOptimisationOutput))
        return value

    @property
    def charts(self) -> 'List[_1078.ParetoOptimisationStrategyChartInformation]':
        '''List[ParetoOptimisationStrategyChartInformation]: 'Charts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Charts, constructor.new(_1078.ParetoOptimisationStrategyChartInformation))
        return value
