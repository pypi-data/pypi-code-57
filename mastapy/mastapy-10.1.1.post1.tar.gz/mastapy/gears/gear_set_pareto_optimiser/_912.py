'''_912.py

DesignSpaceSearchCandidateBase
'''


from typing import Callable, Generic, TypeVar

from mastapy._internal import constructor
from mastapy import _1
from mastapy.gears.analysis import _345
from mastapy._internal.python_net import python_net_import

_DESIGN_SPACE_SEARCH_CANDIDATE_BASE = python_net_import('SMT.MastaAPI.Gears.GearSetParetoOptimiser', 'DesignSpaceSearchCandidateBase')


__docformat__ = 'restructuredtext en'
__all__ = ('DesignSpaceSearchCandidateBase',)


TAnalysis = TypeVar('TAnalysis', bound='_345.AbstractGearSetAnalysis')
TCandidate = TypeVar('TCandidate', bound='DesignSpaceSearchCandidateBase')


class DesignSpaceSearchCandidateBase(_1.APIBase, Generic[TAnalysis, TCandidate]):
    '''DesignSpaceSearchCandidateBase

    This is a mastapy class.

    Generic Types:
        TAnalysis
        TCandidate
    '''

    TYPE = _DESIGN_SPACE_SEARCH_CANDIDATE_BASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'DesignSpaceSearchCandidateBase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def select_candidate(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'SelectCandidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SelectCandidate

    @property
    def design_name(self) -> 'str':
        '''str: 'DesignName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DesignName
