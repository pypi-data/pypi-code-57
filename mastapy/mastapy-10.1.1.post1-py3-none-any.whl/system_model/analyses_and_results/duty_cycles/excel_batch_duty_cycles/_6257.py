'''_6257.py

MASTAFileDetails
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_MASTA_FILE_DETAILS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DutyCycles.ExcelBatchDutyCycles', 'MASTAFileDetails')


__docformat__ = 'restructuredtext en'
__all__ = ('MASTAFileDetails',)


class MASTAFileDetails(_1.APIBase):
    '''MASTAFileDetails

    This is a mastapy class.
    '''

    TYPE = _MASTA_FILE_DETAILS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'MASTAFileDetails.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def file_name(self) -> 'str':
        '''str: 'FileName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FileName

    @property
    def edit_file_name(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'EditFileName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.EditFileName

    @property
    def number_of_design_states(self) -> 'int':
        '''int: 'NumberOfDesignStates' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfDesignStates

    @property
    def input_power_load_specified(self) -> 'bool':
        '''bool: 'InputPowerLoadSpecified' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.InputPowerLoadSpecified
