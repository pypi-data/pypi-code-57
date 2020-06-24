'''_1241.py

ParetoOptimisationVariableBase
'''


from typing import Callable

from mastapy._internal import constructor, conversion
from mastapy.math_utility.optimisation import _1246, _1245
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_PARETO_OPTIMISATION_VARIABLE_BASE = python_net_import('SMT.MastaAPI.MathUtility.Optimisation', 'ParetoOptimisationVariableBase')


__docformat__ = 'restructuredtext en'
__all__ = ('ParetoOptimisationVariableBase',)


class ParetoOptimisationVariableBase(_1.APIBase):
    '''ParetoOptimisationVariableBase

    This is a mastapy class.
    '''

    TYPE = _PARETO_OPTIMISATION_VARIABLE_BASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ParetoOptimisationVariableBase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def property_(self) -> 'str':
        '''str: 'Property' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Property

    @property
    def delete(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'Delete' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Delete

    @property
    def unit(self) -> 'str':
        '''str: 'Unit' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Unit

    @property
    def specification_type(self) -> '_1246.TargetingPropertyTo':
        '''TargetingPropertyTo: 'SpecificationType' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.SpecificationType)
        return constructor.new(_1246.TargetingPropertyTo)(value) if value else None

    @specification_type.setter
    def specification_type(self, value: '_1246.TargetingPropertyTo'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.SpecificationType = value

    @property
    def specify_input_range_as(self) -> '_1245.SpecifyOptimisationInputAs':
        '''SpecifyOptimisationInputAs: 'SpecifyInputRangeAs' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.SpecifyInputRangeAs)
        return constructor.new(_1245.SpecifyOptimisationInputAs)(value) if value else None

    @specify_input_range_as.setter
    def specify_input_range_as(self, value: '_1245.SpecifyOptimisationInputAs'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.SpecifyInputRangeAs = value

    @property
    def value(self) -> 'float':
        '''float: 'Value' is the original name of this property.'''

        return self.wrapped.Value

    @value.setter
    def value(self, value: 'float'):
        self.wrapped.Value = float(value) if value else 0.0
