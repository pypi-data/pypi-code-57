'''_945.py

TableFilter
'''


from typing import Callable, Generic, TypeVar

from mastapy._internal import constructor
from mastapy import _1
from mastapy.gears.analysis import _397
from mastapy._internal.python_net import python_net_import

_TABLE_FILTER = python_net_import('SMT.MastaAPI.Gears.GearSetParetoOptimiser', 'TableFilter')


__docformat__ = 'restructuredtext en'
__all__ = ('TableFilter',)


TAnalysis = TypeVar('TAnalysis', bound='_397.AbstractGearSetAnalysis')
TCandidate = TypeVar('TCandidate', bound='')


class TableFilter(_1.APIBase, Generic[TAnalysis, TCandidate]):
    '''TableFilter

    This is a mastapy class.

    Generic Types:
        TAnalysis
        TCandidate
    '''

    TYPE = _TABLE_FILTER
    __hash__ = None

    def __init__(self, instance_to_wrap: 'TableFilter.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def unit(self) -> 'str':
        '''str: 'Unit' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Unit

    @property
    def remove_filter(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'RemoveFilter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RemoveFilter
