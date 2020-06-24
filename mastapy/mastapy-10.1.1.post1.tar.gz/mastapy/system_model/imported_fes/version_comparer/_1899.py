'''_1899.py

ImportedFEResults
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.imported_fes.version_comparer import _1903
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_IMPORTED_FE_RESULTS = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs.VersionComparer', 'ImportedFEResults')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportedFEResults',)


class ImportedFEResults(_1.APIBase):
    '''ImportedFEResults

    This is a mastapy class.
    '''

    TYPE = _IMPORTED_FE_RESULTS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ImportedFEResults.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def node_results(self) -> 'List[_1903.NodeComparisonResult]':
        '''List[NodeComparisonResult]: 'NodeResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.NodeResults, constructor.new(_1903.NodeComparisonResult))
        return value
