from reamber.sm.lists.notes.SMNoteList import SMNoteList
from reamber.sm.SMMineObject import SMMineObject
from typing import List


class SMMapObjectMines(List[SMMineObject], SMNoteList):
    def data(self) -> List[SMMineObject]:
        return self
