'''_1243.py

PropertyTargetForDominantCandidateSearch
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_PROPERTY_TARGET_FOR_DOMINANT_CANDIDATE_SEARCH = python_net_import('SMT.MastaAPI.MathUtility.Optimisation', 'PropertyTargetForDominantCandidateSearch')


__docformat__ = 'restructuredtext en'
__all__ = ('PropertyTargetForDominantCandidateSearch',)


class PropertyTargetForDominantCandidateSearch(Enum):
    '''PropertyTargetForDominantCandidateSearch

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _PROPERTY_TARGET_FOR_DOMINANT_CANDIDATE_SEARCH
    __hash__ = None

    MAXIMISE = 0
    MINIMISE = 1
    TARGET_VALUE = 2
    DO_NOT_INCLUDE = 3
