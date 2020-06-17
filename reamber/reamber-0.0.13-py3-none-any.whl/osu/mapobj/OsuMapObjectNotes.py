from reamber.base.lists.NoteObjList import NoteObjList
from reamber.osu.lists.notes.OsuHitList import OsuHitList
from reamber.osu.lists.notes.OsuHoldList import OsuHoldList
from dataclasses import dataclass, field
from typing import List


@dataclass
class OsuNoteObjList(NoteObjList):

    hits: OsuHitList = field(default_factory=lambda: OsuHitList())
    holds: OsuHoldList = field(default_factory=lambda: OsuHoldList())

    def __iter__(self):
        yield self.hits
        yield self.holds

    def data(self) -> List:
        # noinspection PyTypeChecker
        return self.hits.data() + self.holds.data()
