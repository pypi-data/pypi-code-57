'''_1845.py

ContactPairWithSelection
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting import _196
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CONTACT_PAIR_WITH_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'ContactPairWithSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('ContactPairWithSelection',)


class ContactPairWithSelection(_1.APIBase):
    '''ContactPairWithSelection

    This is a mastapy class.
    '''

    TYPE = _CONTACT_PAIR_WITH_SELECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ContactPairWithSelection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def select_master_surface(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'SelectMasterSurface' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SelectMasterSurface

    @property
    def select_slave_surface(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'SelectSlaveSurface' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SelectSlaveSurface

    @property
    def select_contacting_master_surface(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'SelectContactingMasterSurface' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SelectContactingMasterSurface

    @property
    def select_contacting_slave_surface(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'SelectContactingSlaveSurface' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SelectContactingSlaveSurface

    @property
    def contact_pair(self) -> '_196.ContactPairReporting':
        '''ContactPairReporting: 'ContactPair' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_196.ContactPairReporting)(self.wrapped.ContactPair) if self.wrapped.ContactPair else None
