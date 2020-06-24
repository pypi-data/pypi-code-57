'''_1901.py

LoadCaseResults
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.imported_fes.version_comparer import _1899
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_LOAD_CASE_RESULTS = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs.VersionComparer', 'LoadCaseResults')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadCaseResults',)


class LoadCaseResults(_1.APIBase):
    '''LoadCaseResults

    This is a mastapy class.
    '''

    TYPE = _LOAD_CASE_RESULTS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadCaseResults.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def status(self) -> 'str':
        '''str: 'Status' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Status

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def imported_fe_results(self) -> 'List[_1899.ImportedFEResults]':
        '''List[ImportedFEResults]: 'ImportedFEResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEResults, constructor.new(_1899.ImportedFEResults))
        return value
