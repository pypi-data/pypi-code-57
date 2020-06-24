'''_5892.py

WaterfallChartSettings
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_WATERFALL_CHART_SETTINGS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'WaterfallChartSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('WaterfallChartSettings',)


class WaterfallChartSettings(_1.APIBase):
    '''WaterfallChartSettings

    This is a mastapy class.
    '''

    TYPE = _WATERFALL_CHART_SETTINGS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'WaterfallChartSettings.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def three_d_view(self) -> 'bool':
        '''bool: 'ThreeDView' is the original name of this property.'''

        return self.wrapped.ThreeDView

    @three_d_view.setter
    def three_d_view(self, value: 'bool'):
        self.wrapped.ThreeDView = bool(value) if value else False

    @property
    def draw_solid_floor(self) -> 'bool':
        '''bool: 'DrawSolidFloor' is the original name of this property.'''

        return self.wrapped.DrawSolidFloor

    @draw_solid_floor.setter
    def draw_solid_floor(self, value: 'bool'):
        self.wrapped.DrawSolidFloor = bool(value) if value else False

    @property
    def flip_axes(self) -> 'bool':
        '''bool: 'FlipAxes' is the original name of this property.'''

        return self.wrapped.FlipAxes

    @flip_axes.setter
    def flip_axes(self, value: 'bool'):
        self.wrapped.FlipAxes = bool(value) if value else False

    @property
    def invert_colours(self) -> 'bool':
        '''bool: 'InvertColours' is the original name of this property.'''

        return self.wrapped.InvertColours

    @invert_colours.setter
    def invert_colours(self, value: 'bool'):
        self.wrapped.InvertColours = bool(value) if value else False

    @property
    def copy_waterfall_data_to_clipboard(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'CopyWaterfallDataToClipboard' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CopyWaterfallDataToClipboard
