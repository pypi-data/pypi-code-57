'''_1288.py

CustomReportItemContainerCollectionBase
'''


from mastapy.utility.report import _1285
from mastapy._internal.python_net import python_net_import

_CUSTOM_REPORT_ITEM_CONTAINER_COLLECTION_BASE = python_net_import('SMT.MastaAPI.Utility.Report', 'CustomReportItemContainerCollectionBase')


__docformat__ = 'restructuredtext en'
__all__ = ('CustomReportItemContainerCollectionBase',)


class CustomReportItemContainerCollectionBase(_1285.CustomReportItem):
    '''CustomReportItemContainerCollectionBase

    This is a mastapy class.
    '''

    TYPE = _CUSTOM_REPORT_ITEM_CONTAINER_COLLECTION_BASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CustomReportItemContainerCollectionBase.TYPE'):
        super().__init__(instance_to_wrap)
