from reamber.quaver.lists.notes.QuaNoteList import QuaNoteList
from reamber.quaver.QuaHoldObject import QuaHoldObject
from typing import List


class QuaMapObjectHolds(List[QuaHoldObject], QuaNoteList):
    def data(self) -> List[QuaHoldObject]:
        return self

    def lengths(self) -> List[float]:
        return self.attribute('length')

    def tailOffsets(self) -> List[float]:
        return [obj() for obj in self.attribute('tailOffset')]
