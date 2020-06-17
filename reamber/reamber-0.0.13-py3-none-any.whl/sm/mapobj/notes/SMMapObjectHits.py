from reamber.sm.lists.notes.SMNoteList import SMNoteList
from reamber.sm.SMHitObject import SMHitObject
from typing import List


class SMMapObjectHits(List[SMHitObject], SMNoteList):
    def data(self) -> List[SMHitObject]:
        return self
