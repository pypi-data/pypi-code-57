"""
Draft Sport
Pick Module
author: hugh@blinkybeach.com
"""
from draft_sport.fantasy.scores.player.score_card import ScoreCard
from nozomi import Decodable, NozomiTime, Immutable
from typing import TypeVar, Type, Any

T = TypeVar('T', bound='Pick')


class Pick(Decodable):

    def __init__(
        self,
        created: NozomiTime,
        manager_id: str,
        score_card: ScoreCard,
        league_id: str
    ) -> None:

        self._created = created
        self._manager_id = manager_id
        self._score_card = score_card
        self._league_id = league_id

        return

    score_card = Immutable(lambda s: s._score_card)

    @classmethod
    def decode(cls: Type[T], data: Any) -> T:
        return cls(
            created=NozomiTime.decode(data['created']),
            manager_id=data['manager_id'],
            score_card=ScoreCard.decode(data['score_card']),
            league_id=data['league_id']
        )
