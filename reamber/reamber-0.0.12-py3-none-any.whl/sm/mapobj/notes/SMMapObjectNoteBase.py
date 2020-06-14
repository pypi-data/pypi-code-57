from reamber.base.lists.notes.NoteList import TimedList
from typing import List, Type
from abc import ABC


class SMMapObjectNoteBase(TimedList, ABC):
    def data(self) -> List[Type]: pass

