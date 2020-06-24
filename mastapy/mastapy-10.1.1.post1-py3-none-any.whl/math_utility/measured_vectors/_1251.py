'''_1251.py

OverridableDisplacementBoundaryCondition
'''


from mastapy._internal.implicit import overridable
from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_OVERRIDABLE_DISPLACEMENT_BOUNDARY_CONDITION = python_net_import('SMT.MastaAPI.MathUtility.MeasuredVectors', 'OverridableDisplacementBoundaryCondition')


__docformat__ = 'restructuredtext en'
__all__ = ('OverridableDisplacementBoundaryCondition',)


class OverridableDisplacementBoundaryCondition(_1.APIBase):
    '''OverridableDisplacementBoundaryCondition

    This is a mastapy class.
    '''

    TYPE = _OVERRIDABLE_DISPLACEMENT_BOUNDARY_CONDITION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'OverridableDisplacementBoundaryCondition.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def x(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'X' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.X) if self.wrapped.X else None

    @x.setter
    def x(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.X = value

    @property
    def y(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'Y' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.Y) if self.wrapped.Y else None

    @y.setter
    def y(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.Y = value

    @property
    def z(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'Z' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.Z) if self.wrapped.Z else None

    @z.setter
    def z(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.Z = value

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.'''

        return self.wrapped.Name

    @name.setter
    def name(self, value: 'str'):
        self.wrapped.Name = str(value) if value else None
