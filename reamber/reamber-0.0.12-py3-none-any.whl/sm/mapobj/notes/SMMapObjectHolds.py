from reamber.sm.lists.notes.SMNoteList import SMNoteList
from reamber.sm.SMHoldObject import SMHoldObject
from typing import List


class SMMapObjectHolds(List[SMHoldObject], SMNoteList):
    def data(self) -> List[SMHoldObject]:
        return self

    def lengths(self) -> List[float]:
        return self.attribute('length')

    def tailOffsets(self) -> List[float]:
        return [obj() for obj in self.attribute('tailOffset')]
