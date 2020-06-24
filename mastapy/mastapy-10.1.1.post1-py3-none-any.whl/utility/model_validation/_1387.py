'''_1387.py

Status
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.utility.model_validation import _1428
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_STATUS = python_net_import('SMT.MastaAPI.Utility.ModelValidation', 'Status')


__docformat__ = 'restructuredtext en'
__all__ = ('Status',)


class Status(_1.APIBase):
    '''Status

    This is a mastapy class.
    '''

    TYPE = _STATUS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'Status.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def has_errors(self) -> 'bool':
        '''bool: 'HasErrors' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HasErrors

    @property
    def error_count(self) -> 'int':
        '''int: 'ErrorCount' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ErrorCount

    @property
    def has_warnings(self) -> 'bool':
        '''bool: 'HasWarnings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HasWarnings

    @property
    def warning_count(self) -> 'int':
        '''int: 'WarningCount' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.WarningCount

    @property
    def has_information(self) -> 'bool':
        '''bool: 'HasInformation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HasInformation

    @property
    def information_count(self) -> 'int':
        '''int: 'InformationCount' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.InformationCount

    @property
    def has_errors_or_warnings(self) -> 'bool':
        '''bool: 'HasErrorsOrWarnings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HasErrorsOrWarnings

    @property
    def errors(self) -> 'List[_1428.StatusItem]':
        '''List[StatusItem]: 'Errors' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Errors, constructor.new(_1428.StatusItem))
        return value

    @property
    def warnings(self) -> 'List[_1428.StatusItem]':
        '''List[StatusItem]: 'Warnings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Warnings, constructor.new(_1428.StatusItem))
        return value
