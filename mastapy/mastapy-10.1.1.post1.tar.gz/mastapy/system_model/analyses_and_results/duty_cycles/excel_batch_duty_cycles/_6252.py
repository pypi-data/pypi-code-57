'''_6252.py

ExcelBatchDutyCycleCreator
'''


from mastapy.system_model.analyses_and_results.duty_cycles.excel_batch_duty_cycles import _6253
from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_EXCEL_BATCH_DUTY_CYCLE_CREATOR = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DutyCycles.ExcelBatchDutyCycles', 'ExcelBatchDutyCycleCreator')


__docformat__ = 'restructuredtext en'
__all__ = ('ExcelBatchDutyCycleCreator',)


class ExcelBatchDutyCycleCreator(_1.APIBase):
    '''ExcelBatchDutyCycleCreator

    This is a mastapy class.
    '''

    TYPE = _EXCEL_BATCH_DUTY_CYCLE_CREATOR
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ExcelBatchDutyCycleCreator.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def batch_details(self) -> '_6253.ExcelBatchDutyCycleSpectraCreatorDetails':
        '''ExcelBatchDutyCycleSpectraCreatorDetails: 'BatchDetails' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6253.ExcelBatchDutyCycleSpectraCreatorDetails)(self.wrapped.BatchDetails) if self.wrapped.BatchDetails else None
