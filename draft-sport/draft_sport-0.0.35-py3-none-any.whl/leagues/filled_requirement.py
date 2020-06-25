"""
Draft Sport API
Filled Requirement Module
author: hugh@blinkybeach.com
"""
from nozomi import Immutable
from typing import List, Union
from draft_sport.leagues.pick import Pick
from draft_sport.leagues.position_requirement import PositionRequirement
from draft_sport.leagues.category_requirement import CategoryRequirement

Requirement = Union[PositionRequirement, CategoryRequirement]


class FilledRequirement:
    """
    Utility class coralling Requirement & Player data. Useful for client
    presentation purposes. There is no equivalent object in the
    Draft Sport API
    """

    def __init__(
        self,
        requirement: Requirement,
        picks: List[Pick]
    ) -> None:

        self._picks = picks
        self._requirement = requirement

        return

    picks = Immutable(lambda s: s._picks)
    name = Immutable(lambda s: s._compute_requirement_name())
    position_name = Immutable(lambda s: s._requirement.position_name)
    count = Immutable(lambda s: s._requirement.count)

    is_position: bool = Immutable(
        lambda s: isinstance(s._requirement, PositionRequirement)
    )
    is_category: bool = Immutable(
        lambda s: isinstance(s._requirement, CategoryRequirement)
    )
    is_plural: bool = Immutable(lambda s: s.count > 1)
    number_filled: int = Immutable(lambda s: len(s.picks))
    empty: bool = Immutable(lambda s: len(s.picks) < 1)
    satisfied: bool = Immutable(lambda s: len(s.picks) == s.count)
    not_satisfied: bool = Immutable(lambda s: not s.satisfied)

    def _compute_requirement_name(self) -> str:

        if isinstance(self._requirement, CategoryRequirement):
            name = self._requirement.category.name
            return name[0].upper() + name[1:].lower()

        if isinstance(self._requirement, PositionRequirement):
            return self._requirement.position_name

        raise TypeError
