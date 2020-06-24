'''_67.py

ShaftSurfaceRoughness
'''


from mastapy._internal.implicit import enum_with_selected_value, overridable
from mastapy.shafts import _65
from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_SHAFT_SURFACE_ROUGHNESS = python_net_import('SMT.MastaAPI.Shafts', 'ShaftSurfaceRoughness')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftSurfaceRoughness',)


class ShaftSurfaceRoughness(_1.APIBase):
    '''ShaftSurfaceRoughness

    This is a mastapy class.
    '''

    TYPE = _SHAFT_SURFACE_ROUGHNESS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftSurfaceRoughness.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def surface_finish(self) -> 'enum_with_selected_value.EnumWithSelectedValue_SurfaceFinishes':
        '''enum_with_selected_value.EnumWithSelectedValue_SurfaceFinishes: 'SurfaceFinish' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_SurfaceFinishes)(self.wrapped.SurfaceFinish) if self.wrapped.SurfaceFinish else None

    @surface_finish.setter
    def surface_finish(self, value: 'enum_with_selected_value.EnumWithSelectedValue_SurfaceFinishes.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_SurfaceFinishes.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_SurfaceFinishes.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.SurfaceFinish = value

    @property
    def surface_roughness(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'SurfaceRoughness' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.SurfaceRoughness) if self.wrapped.SurfaceRoughness else None

    @surface_roughness.setter
    def surface_roughness(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.SurfaceRoughness = value
