'''_1290.py

CustomReportKey
'''


from mastapy.utility.databases import _1339
from mastapy._internal.python_net import python_net_import

_CUSTOM_REPORT_KEY = python_net_import('SMT.MastaAPI.Utility.Report', 'CustomReportKey')


__docformat__ = 'restructuredtext en'
__all__ = ('CustomReportKey',)


class CustomReportKey(_1339.DatabaseKey):
    '''CustomReportKey

    This is a mastapy class.
    '''

    TYPE = _CUSTOM_REPORT_KEY

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CustomReportKey.TYPE'):
        super().__init__(instance_to_wrap)
