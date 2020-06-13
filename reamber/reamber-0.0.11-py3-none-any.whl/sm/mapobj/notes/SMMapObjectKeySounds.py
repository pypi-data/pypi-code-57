from reamber.sm.lists.notes.SMNoteList import SMNoteList
from reamber.sm.SMKeySoundObject import SMKeySoundObject
from typing import List


class SMMapObjectKeySounds(List[SMKeySoundObject], SMNoteList):
    def data(self) -> List[SMKeySoundObject]:
        return self
