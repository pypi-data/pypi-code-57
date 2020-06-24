'''_216.py

CMSResults
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CMS_RESULTS = python_net_import('SMT.MastaAPI.NodalAnalysis.ComponentModeSynthesis', 'CMSResults')


__docformat__ = 'restructuredtext en'
__all__ = ('CMSResults',)


class CMSResults(_1.APIBase):
    '''CMSResults

    This is a mastapy class.
    '''

    TYPE = _CMS_RESULTS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CMSResults.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def calculate_displacements(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'CalculateDisplacements' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CalculateDisplacements
