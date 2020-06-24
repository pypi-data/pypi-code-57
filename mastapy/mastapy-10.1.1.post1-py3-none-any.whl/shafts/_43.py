'''_43.py

ShaftDamageResultsTableAndChart
'''


from mastapy.utility.enums import _59
from mastapy._internal import constructor, conversion
from mastapy.utility.report import _60
from mastapy._internal.python_net import python_net_import

_SHAFT_DAMAGE_RESULTS_TABLE_AND_CHART = python_net_import('SMT.MastaAPI.Shafts', 'ShaftDamageResultsTableAndChart')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftDamageResultsTableAndChart',)


class ShaftDamageResultsTableAndChart(_60.CustomReportChart):
    '''ShaftDamageResultsTableAndChart

    This is a mastapy class.
    '''

    TYPE = _SHAFT_DAMAGE_RESULTS_TABLE_AND_CHART
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftDamageResultsTableAndChart.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def display(self) -> '_59.TableAndChartOptions':
        '''TableAndChartOptions: 'Display' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.Display)
        return constructor.new(_59.TableAndChartOptions)(value) if value else None

    @display.setter
    def display(self, value: '_59.TableAndChartOptions'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.Display = value
