"""
Draft Sport Python
Filled Composition Class
author: hugh@blinkbeach.com
"""
from typing import List
from nozomi import Immutable
from draft_sport.leagues.filled_requirement import FilledRequirement


class FilledComposition:
    """
    A utility class coralling Composition and Player data into a combined unit.
    Useful on the client side for presentation purposes. There is no
    equivalent object in the Draft Sport API
    """

    def __init__(
        self,
        requirements: List[FilledRequirement]
    ) -> None:

        self._requirements = requirements

        return

    requirements: List[FilledRequirement] = Immutable(lambda s: s._requirements)
