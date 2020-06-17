from reamber.base.lists.notes.NoteList import TimedList
from typing import List, Type
from abc import ABC

from reamber.quaver.QuaNoteObjectMeta import QuaNoteObjectMeta


class QuaMapObjectNoteBase(TimedList, ABC):
    def data(self) -> List[Type[QuaNoteObjectMeta]]: pass

    def keySoundsList(self):
        return self.attribute('keySounds')
