'''_1229.py

CustomTable
'''


from mastapy._internal import constructor
from mastapy.utility.report import _1411, _1420
from mastapy._internal.python_net import python_net_import

_CUSTOM_TABLE = python_net_import('SMT.MastaAPI.Utility.Report', 'CustomTable')


__docformat__ = 'restructuredtext en'
__all__ = ('CustomTable',)


class CustomTable(_1411.CustomReportMultiPropertyItem['_1420.CustomRow']):
    '''CustomTable

    This is a mastapy class.
    '''

    TYPE = _CUSTOM_TABLE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CustomTable.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def is_main_report_item(self) -> 'bool':
        '''bool: 'IsMainReportItem' is the original name of this property.'''

        return self.wrapped.IsMainReportItem

    @is_main_report_item.setter
    def is_main_report_item(self, value: 'bool'):
        self.wrapped.IsMainReportItem = bool(value) if value else False
