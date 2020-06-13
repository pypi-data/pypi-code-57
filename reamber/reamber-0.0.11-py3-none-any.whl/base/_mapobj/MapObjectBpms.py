from typing import List
from reamber.base.BpmObject import BpmObject
import pandas as pd


class MapObjectBpms(List[BpmObject]):

    def __init__(self, *args):
        list.__init__(self, *args)

    def bpmDf(self) -> pd.DataFrame:
        return pd.DataFrame({'noteObjects' : self})

    def bpmPointsSorted(self) -> List[BpmObject]:
        """ Returns a copy of Sorted BPMs """
        return sorted(self, key=lambda tp: tp.offset)

    def addBpmOffsets(self, by: float):
        """ Move all bpms by a specific ms """
        for bpm in self: bpm.offset += by