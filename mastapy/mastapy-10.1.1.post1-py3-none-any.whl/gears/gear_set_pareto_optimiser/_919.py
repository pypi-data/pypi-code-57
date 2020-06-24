'''_919.py

InputSliderForPareto
'''


from typing import Generic, TypeVar

from mastapy._internal import constructor
from mastapy import _1
from mastapy.gears.analysis import _345
from mastapy._internal.python_net import python_net_import

_INPUT_SLIDER_FOR_PARETO = python_net_import('SMT.MastaAPI.Gears.GearSetParetoOptimiser', 'InputSliderForPareto')


__docformat__ = 'restructuredtext en'
__all__ = ('InputSliderForPareto',)


TAnalysis = TypeVar('TAnalysis', bound='_345.AbstractGearSetAnalysis')
TCandidate = TypeVar('TCandidate', bound='')


class InputSliderForPareto(_1.APIBase, Generic[TAnalysis, TCandidate]):
    '''InputSliderForPareto

    This is a mastapy class.

    Generic Types:
        TAnalysis
        TCandidate
    '''

    TYPE = _INPUT_SLIDER_FOR_PARETO
    __hash__ = None

    def __init__(self, instance_to_wrap: 'InputSliderForPareto.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def value(self) -> 'float':
        '''float: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Value

    @property
    def property_(self) -> 'str':
        '''str: 'Property' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Property
