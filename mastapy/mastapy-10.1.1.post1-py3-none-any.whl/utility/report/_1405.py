'''_1405.py

CustomReportHtmlItem
'''


from mastapy.utility.report import _1403
from mastapy._internal.python_net import python_net_import

_CUSTOM_REPORT_HTML_ITEM = python_net_import('SMT.MastaAPI.Utility.Report', 'CustomReportHtmlItem')


__docformat__ = 'restructuredtext en'
__all__ = ('CustomReportHtmlItem',)


class CustomReportHtmlItem(_1403.CustomReportDefinitionItem):
    '''CustomReportHtmlItem

    This is a mastapy class.
    '''

    TYPE = _CUSTOM_REPORT_HTML_ITEM
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CustomReportHtmlItem.TYPE'):
        super().__init__(instance_to_wrap)
