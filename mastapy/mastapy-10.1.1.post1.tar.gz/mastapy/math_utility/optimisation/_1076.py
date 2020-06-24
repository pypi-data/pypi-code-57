'''_1076.py

ParetoOptimisationStrategyChartInformation
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.math_utility.optimisation import _1075
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_PARETO_OPTIMISATION_STRATEGY_CHART_INFORMATION = python_net_import('SMT.MastaAPI.MathUtility.Optimisation', 'ParetoOptimisationStrategyChartInformation')


__docformat__ = 'restructuredtext en'
__all__ = ('ParetoOptimisationStrategyChartInformation',)


class ParetoOptimisationStrategyChartInformation(_1.APIBase):
    '''ParetoOptimisationStrategyChartInformation

    This is a mastapy class.
    '''

    TYPE = _PARETO_OPTIMISATION_STRATEGY_CHART_INFORMATION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ParetoOptimisationStrategyChartInformation.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def select_chart_type(self) -> 'ParetoOptimisationStrategyChartInformation.ScatterOrBarChart':
        '''ScatterOrBarChart: 'SelectChartType' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.SelectChartType)
        return constructor.new(ParetoOptimisationStrategyChartInformation.ScatterOrBarChart)(value) if value else None

    @select_chart_type.setter
    def select_chart_type(self, value: 'ParetoOptimisationStrategyChartInformation.ScatterOrBarChart'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.SelectChartType = value

    @property
    def remove_chart(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'RemoveChart' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RemoveChart

    @property
    def add_bar(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'AddBar' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AddBar

    @property
    def chart_name(self) -> 'str':
        '''str: 'ChartName' is the original name of this property.'''

        return self.wrapped.ChartName

    @chart_name.setter
    def chart_name(self, value: 'str'):
        self.wrapped.ChartName = str(value) if value else None

    @property
    def bars(self) -> 'List[_1075.ParetoOptimisationStrategyBars]':
        '''List[ParetoOptimisationStrategyBars]: 'Bars' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bars, constructor.new(_1075.ParetoOptimisationStrategyBars))
        return value
