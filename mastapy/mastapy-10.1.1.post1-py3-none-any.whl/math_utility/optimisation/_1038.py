'''_1038.py

InputSetter
'''


from typing import Generic, TypeVar

from mastapy._internal import constructor
from mastapy.math_utility.optimisation import _1239
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_INPUT_SETTER = python_net_import('SMT.MastaAPI.MathUtility.Optimisation', 'InputSetter')


__docformat__ = 'restructuredtext en'
__all__ = ('InputSetter',)


T = TypeVar('T')


class InputSetter(_1.APIBase, Generic[T]):
    '''InputSetter

    This is a mastapy class.

    Generic Types:
        T
    '''

    TYPE = _INPUT_SETTER
    __hash__ = None

    def __init__(self, instance_to_wrap: 'InputSetter.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def fix_this_property(self) -> 'bool':
        '''bool: 'FixThisProperty' is the original name of this property.'''

        return self.wrapped.FixThisProperty

    @fix_this_property.setter
    def fix_this_property(self, value: 'bool'):
        self.wrapped.FixThisProperty = bool(value) if value else False

    @property
    def last_path_object_name(self) -> 'str':
        '''str: 'LastPathObjectName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LastPathObjectName

    @property
    def value(self) -> 'float':
        '''float: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Value

    @property
    def optimiser_input(self) -> '_1239.ParetoOptimisationInput':
        '''ParetoOptimisationInput: 'OptimiserInput' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1239.ParetoOptimisationInput)(self.wrapped.OptimiserInput) if self.wrapped.OptimiserInput else None

    @property
    def candidate(self) -> 'T':
        '''T: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(T)(self.wrapped.Candidate) if self.wrapped.Candidate else None
