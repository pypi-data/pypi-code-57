'''_1445.py

StockDrawings
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_STOCK_DRAWINGS = python_net_import('SMT.MastaAPI.Utility.CadExport', 'StockDrawings')


__docformat__ = 'restructuredtext en'
__all__ = ('StockDrawings',)


class StockDrawings(Enum):
    '''StockDrawings

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _STOCK_DRAWINGS
    __hash__ = None

    GEAR_CHAMFER_DETAIL = 0
    RACK_WITH_SEMI_TOPPING = 1
    RACK_WITHOUT_SEMI_TOPPING = 2
