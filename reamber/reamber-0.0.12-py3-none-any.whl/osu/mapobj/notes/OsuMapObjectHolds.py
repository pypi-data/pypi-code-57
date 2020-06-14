from reamber.osu.lists.notes.OsuNoteList import OsuNoteList
from reamber.osu.OsuHoldObject import OsuHoldObject
from typing import List


class OsuMapObjectHolds(List[OsuHoldObject], OsuNoteList):
    def data(self) -> List[OsuHoldObject]:
        return self

    def lengths(self) -> List[float]:
        return self.attribute('length')

    def tailOffsets(self) -> List[float]:
        return [obj() for obj in self.attribute('tailOffset')]
