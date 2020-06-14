from typing import List
from reamber.base.BpmObject import BpmObject
from reamber.base.lists.TimedList import TimedList


class MapObjectBpms(List[BpmObject], TimedList):

    def data(self) -> List[BpmObject]:
        return self

    def bpms(self) -> List[float]:
        return self.attribute('bpm')
