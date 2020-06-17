from reamber.base.lists.TimedList import TimedList
from reamber.quaver.QuaSvObject import QuaSvObject
from typing import List


class QuaMapObjectSvs(List[QuaSvObject], TimedList):

    def data(self) -> List[QuaSvObject]:
        return self

    def multipliers(self) -> List[float]:
        return self.attribute('multiplier')
