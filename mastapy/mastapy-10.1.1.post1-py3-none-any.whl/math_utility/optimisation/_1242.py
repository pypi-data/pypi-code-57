'''_1242.py

ParetoOptimistaionVariable
'''


from mastapy.math_utility.optimisation import _1243, _1241
from mastapy._internal import constructor, conversion
from mastapy._internal.python_net import python_net_import

_PARETO_OPTIMISTAION_VARIABLE = python_net_import('SMT.MastaAPI.MathUtility.Optimisation', 'ParetoOptimistaionVariable')


__docformat__ = 'restructuredtext en'
__all__ = ('ParetoOptimistaionVariable',)


class ParetoOptimistaionVariable(_1241.ParetoOptimisationVariableBase):
    '''ParetoOptimistaionVariable

    This is a mastapy class.
    '''

    TYPE = _PARETO_OPTIMISTAION_VARIABLE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ParetoOptimistaionVariable.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def property_target_for_dominant_candidate_search(self) -> '_1243.PropertyTargetForDominantCandidateSearch':
        '''PropertyTargetForDominantCandidateSearch: 'PropertyTargetForDominantCandidateSearch' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.PropertyTargetForDominantCandidateSearch)
        return constructor.new(_1243.PropertyTargetForDominantCandidateSearch)(value) if value else None

    @property_target_for_dominant_candidate_search.setter
    def property_target_for_dominant_candidate_search(self, value: '_1243.PropertyTargetForDominantCandidateSearch'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.PropertyTargetForDominantCandidateSearch = value
