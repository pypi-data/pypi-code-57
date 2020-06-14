from reamber.base.lists.notes.NoteList import TimedList
from typing import List, Type
from abc import ABC

from reamber.osu.OsuNoteObjectMeta import OsuNoteObjectMeta
from reamber.osu.OsuSampleSet import OsuSampleSet


class OsuMapObjectNoteBase(TimedList, ABC):
    def data(self) -> List[Type[OsuNoteObjectMeta]]: pass

    def volumes(self) -> List[float]:
        return self.attribute('volumes')

    def hitsoundFiles(self) -> List[str]:
        return self.attribute('hitsoundFile')

    def sampleSets(self) -> List[OsuSampleSet]:
        return self.attribute('sampleSet')

    def hitsoundSets(self) -> List[OsuSampleSet]:
        return self.attribute('hitsoundSet')

    def customSets(self) -> List[OsuSampleSet]:
        return self.attribute('customSet')

    def additionSets(self) -> List[OsuSampleSet]:
        return self.attribute('additionSet')
