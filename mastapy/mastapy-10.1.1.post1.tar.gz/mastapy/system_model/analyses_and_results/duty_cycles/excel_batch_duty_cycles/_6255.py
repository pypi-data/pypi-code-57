'''_6255.py

ExcelSheet
'''


from mastapy import _1
from mastapy._internal.python_net import python_net_import

_EXCEL_SHEET = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DutyCycles.ExcelBatchDutyCycles', 'ExcelSheet')


__docformat__ = 'restructuredtext en'
__all__ = ('ExcelSheet',)


class ExcelSheet(_1.APIBase):
    '''ExcelSheet

    This is a mastapy class.
    '''

    TYPE = _EXCEL_SHEET
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ExcelSheet.TYPE'):
        super().__init__(instance_to_wrap)
