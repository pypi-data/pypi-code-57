'''_1756.py

ScalingDrawStyle
'''


from mastapy._internal import constructor
from mastapy._internal.implicit import overridable
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_SCALING_DRAW_STYLE = python_net_import('SMT.MastaAPI.SystemModel.Drawing', 'ScalingDrawStyle')


__docformat__ = 'restructuredtext en'
__all__ = ('ScalingDrawStyle',)


class ScalingDrawStyle(_1.APIBase):
    '''ScalingDrawStyle

    This is a mastapy class.
    '''

    TYPE = _SCALING_DRAW_STYLE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ScalingDrawStyle.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def scale(self) -> 'float':
        '''float: 'Scale' is the original name of this property.'''

        return self.wrapped.Scale

    @scale.setter
    def scale(self, value: 'float'):
        self.wrapped.Scale = float(value) if value else 0.0

    @property
    def max_scale(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'MaxScale' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.MaxScale) if self.wrapped.MaxScale else None

    @max_scale.setter
    def max_scale(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.MaxScale = value

    @property
    def min_scale(self) -> 'float':
        '''float: 'MinScale' is the original name of this property.'''

        return self.wrapped.MinScale

    @min_scale.setter
    def min_scale(self, value: 'float'):
        self.wrapped.MinScale = float(value) if value else 0.0
