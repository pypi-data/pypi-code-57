'''_66.py

ShaftSurfaceFinishSection
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy.shafts import _67, _47
from mastapy._internal.python_net import python_net_import

_SHAFT_SURFACE_FINISH_SECTION = python_net_import('SMT.MastaAPI.Shafts', 'ShaftSurfaceFinishSection')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftSurfaceFinishSection',)


class ShaftSurfaceFinishSection(_47.ShaftFeature):
    '''ShaftSurfaceFinishSection

    This is a mastapy class.
    '''

    TYPE = _SHAFT_SURFACE_FINISH_SECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftSurfaceFinishSection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def add_new_surface_finish_section(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'AddNewSurfaceFinishSection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AddNewSurfaceFinishSection

    @property
    def length(self) -> 'float':
        '''float: 'Length' is the original name of this property.'''

        return self.wrapped.Length

    @length.setter
    def length(self, value: 'float'):
        self.wrapped.Length = float(value) if value else 0.0

    @property
    def surface_roughness(self) -> '_67.ShaftSurfaceRoughness':
        '''ShaftSurfaceRoughness: 'SurfaceRoughness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_67.ShaftSurfaceRoughness)(self.wrapped.SurfaceRoughness) if self.wrapped.SurfaceRoughness else None
