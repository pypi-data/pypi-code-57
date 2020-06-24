'''_5889.py

OrderCutsChartSettings
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_ORDER_CUTS_CHART_SETTINGS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'OrderCutsChartSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('OrderCutsChartSettings',)


class OrderCutsChartSettings(_1.APIBase):
    '''OrderCutsChartSettings

    This is a mastapy class.
    '''

    TYPE = _ORDER_CUTS_CHART_SETTINGS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'OrderCutsChartSettings.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def speed_on_x_axis(self) -> 'bool':
        '''bool: 'SpeedOnXAxis' is the original name of this property.'''

        return self.wrapped.SpeedOnXAxis

    @speed_on_x_axis.setter
    def speed_on_x_axis(self, value: 'bool'):
        self.wrapped.SpeedOnXAxis = bool(value) if value else False
