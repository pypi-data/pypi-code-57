'''_280.py

ClippingPlane
'''


from mastapy._internal import constructor, conversion
from mastapy.math_utility import _289
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CLIPPING_PLANE = python_net_import('SMT.MastaAPI.Geometry', 'ClippingPlane')


__docformat__ = 'restructuredtext en'
__all__ = ('ClippingPlane',)


class ClippingPlane(_1.APIBase):
    '''ClippingPlane

    This is a mastapy class.
    '''

    TYPE = _CLIPPING_PLANE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClippingPlane.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def is_enabled(self) -> 'bool':
        '''bool: 'IsEnabled' is the original name of this property.'''

        return self.wrapped.IsEnabled

    @is_enabled.setter
    def is_enabled(self, value: 'bool'):
        self.wrapped.IsEnabled = bool(value) if value else False

    @property
    def axis(self) -> '_289.Axis':
        '''Axis: 'Axis' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.Axis)
        return constructor.new(_289.Axis)(value) if value else None

    @axis.setter
    def axis(self, value: '_289.Axis'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.Axis = value

    @property
    def is_flipped(self) -> 'bool':
        '''bool: 'IsFlipped' is the original name of this property.'''

        return self.wrapped.IsFlipped

    @is_flipped.setter
    def is_flipped(self, value: 'bool'):
        self.wrapped.IsFlipped = bool(value) if value else False
