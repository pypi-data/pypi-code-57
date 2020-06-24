'''_929.py

OptimisationTarget
'''


from typing import List, Generic, TypeVar

from mastapy._internal import constructor, conversion
from mastapy.math_utility.optimisation import _1037
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_OPTIMISATION_TARGET = python_net_import('SMT.MastaAPI.Gears.GearSetParetoOptimiser', 'OptimisationTarget')


__docformat__ = 'restructuredtext en'
__all__ = ('OptimisationTarget',)


T = TypeVar('T')


class OptimisationTarget(_1.APIBase, Generic[T]):
    '''OptimisationTarget

    This is a mastapy class.

    Generic Types:
        T
    '''

    TYPE = _OPTIMISATION_TARGET
    __hash__ = None

    def __init__(self, instance_to_wrap: 'OptimisationTarget.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def input_setters(self) -> 'List[_1037.InputSetter[T]]':
        '''List[InputSetter[T]]: 'InputSetters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.InputSetters, constructor.new(_1037.InputSetter)[T])
        return value
