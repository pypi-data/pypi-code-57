'''_1336.py

TableAndChartOptions
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_TABLE_AND_CHART_OPTIONS = python_net_import('SMT.MastaAPI.Utility.Enums', 'TableAndChartOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('TableAndChartOptions',)


class TableAndChartOptions(Enum):
    '''TableAndChartOptions

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _TABLE_AND_CHART_OPTIONS

    __hash__ = None

    CHART_THEN_TABLE = 0
    TABLE_THEN_CHART = 1
    TABLE = 2
    CHART = 3
