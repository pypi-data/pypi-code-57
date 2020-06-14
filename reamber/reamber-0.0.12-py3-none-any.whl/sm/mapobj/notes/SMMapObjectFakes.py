from reamber.sm.lists.notes.SMNoteList import SMNoteList
from reamber.sm.SMFakeObject import SMFakeObject
from typing import List


class SMMapObjectFakes(List[SMFakeObject], SMNoteList):
    def data(self) -> List[SMFakeObject]:
        return self
