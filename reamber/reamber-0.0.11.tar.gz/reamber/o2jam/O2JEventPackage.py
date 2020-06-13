from __future__ import annotations

import logging
import struct
from collections import deque
from dataclasses import dataclass, field
from typing import List, Union, Dict

from reamber.o2jam.O2JBpmObj import O2JBpmObj
from reamber.o2jam.O2JHitObj import O2JHitObj
from reamber.o2jam.O2JHoldObj import O2JHoldObj

log = logging.getLogger(__name__)

class O2JConst:

    # These data are required to find out which notes are hits and holds
    HIT_BYTES      : bytes = b'\x00'
    HOLD_HEAD_BYTES: bytes = b'\x02'
    HOLD_TAIL_BYTES: bytes = b'\x03'
    # HIT            : int   = 0  # Not very useful
    # HOLD_HEAD      : int   = 2  # Not very useful
    # HOLD_TAIL      : int   = 3  # Not very useful


class O2JNoteChannel:
    MEASURE_FRACTION: int = 0
    BPM_CHANGE      : int = 1
    COL_1           : int = 2
    COL_2           : int = 3
    COL_3           : int = 4
    COL_4           : int = 5
    COL_5           : int = 6
    COL_6           : int = 7
    COL_7           : int = 8
    COL_RANGE       : range = range(2, 9)
    AUTOPLAY_1      : int = 9
    AUTOPLAY_2      : int = 10
    AUTOPLAY_3      : int = 11
    AUTOPLAY_4      : int = 12
    AUTOPLAY_5      : int = 13
    AUTOPLAY_6      : int = 14
    AUTOPLAY_7      : int = 15
    AUTOPLAY_8      : int = 16
    AUTOPLAY_9      : int = 17
    AUTOPLAY_10     : int = 18
    AUTOPLAY_11     : int = 19
    AUTOPLAY_12     : int = 20
    AUTOPLAY_13     : int = 21
    AUTOPLAY_14     : int = 22
    AUTOPLAY_RANGE  : range = range(9, 23)
    # Is there more?
    # Don't worry about the size of this obj, all of them are static.


@dataclass
class O2JEventMeasureChange:
    # When the channel is 0(fractional measure), the 4 bytes are a float,
    # indicating how much of the measure is actually used,
    # so if the value is 0.75, the size of this measure will be only 75% of a normal measure.
    fracLength: float = 1.0

@dataclass
class O2JHit:
    # The purpose of this class is to facilitate conversion from measures into offset
    column: int = 0
    measure: float = 0.0  # Note that this measure is relative to the previous BPM

@dataclass
class O2JHold:
    column: int = 0
    measure: float = 0.0
    measureEnd: float = 0.0

@dataclass
class O2JEventPackage:
    measure: int = 0  # Len 4 (Int)
    channel: int = -1  # Len 2 (Short)
    # There's a Len 2 (Short) indicating how many events there are.
    # Then it's followed by that amount of events.
    events: List[Union[O2JBpmObj, O2JHitObj, O2JHoldObj, O2JEventMeasureChange]] =\
        field(default_factory=lambda: [])

    @staticmethod
    def readEventPackages(data: bytes, lvlPkgCounts: List[int]) -> List[List[O2JEventPackage]]:
        """ Reads all events, this data found after the metadata (300:)
        :param lvlPkgCounts: The count of pkgs per level
        :param data: All the event data in bytes.
        """
        # Don't think we can reliably get all the offsets of notes, we'll firstly find their measures, then calculate
        # the offsets separately.
        # I have doubts because of bpm changes

        # Because of this, we have to parse LNs in a different wave instead of dynamically like stepmania.

        # Additional variables
        # O2JHit.measure
        # O2JHold.measure
        # O2JHold.tailMeasure

        lvls: List[List[O2JEventPackage]] = []
        dataQ = deque(data)

        # Column, Offset
        holdBuffer: Dict[int, O2JHoldObj] = {}

        # For each level, we will read the required amount of packages, then go to the next
        for lvlPkgI, lvlPkgCount in enumerate(lvlPkgCounts):
            log.debug(f"Loading New Package with {lvlPkgCount} Packages")
            # noinspection PyTypeChecker
            lvlPkg: List[O2JEventPackage] = [None] * lvlPkgCount
            for pkgI in range(0, lvlPkgCount):
                if len(dataQ) == 0: break
                pkg = O2JEventPackage()
                pkgData = []
                for i in range(8): pkgData.append(dataQ.popleft())

                pkg.measure = struct.unpack("<i", bytes(pkgData[0:4]))[0]
                pkg.channel = struct.unpack("<h", bytes(pkgData[4:6]))[0]
                eventCount  = struct.unpack("<h", bytes(pkgData[6:8]))[0]

                eventsData = []
                for i in range(4 * eventCount): eventsData.append(dataQ.popleft())
                eventsData = bytes(eventsData)

                if pkg.channel in O2JNoteChannel.COL_RANGE:
                    pkg.events += O2JEventPackage.readEventsNote(eventsData,
                                                                 pkg.channel - 2,  # Package CHN - 2 is column
                                                                 holdBuffer,
                                                                 pkg.measure)
                elif pkg.channel == O2JNoteChannel.BPM_CHANGE:
                    pkg.events += O2JEventPackage.readEventsBpm(eventsData,
                                                                pkg.measure)
                elif pkg.channel == O2JNoteChannel.MEASURE_FRACTION:
                    measureFrac = O2JEventPackage.readEventsMeasure(eventsData)
                    pkg.events.append(O2JEventMeasureChange(measureFrac))
                else:
                    # log.debug(f"{currMeasure} count: {eventCount}, chn: {pkg.channel}")
                    pass
                lvlPkg[pkgI] = pkg
            lvls.append(lvlPkg)
        return lvls

    @staticmethod
    def readEventsMeasure(eventsData: bytes) -> float:
        log.warning("Fractional measure isn't confidently implemented, conversion may fail.")
        return struct.unpack("<f", eventsData[0:4])[0]

    @staticmethod
    def readEventsBpm(eventsData: bytes, currMeasure: float) -> List[O2JBpmObj]:
        eventCount = int(len(eventsData) / 4)
        bpms = []

        for i in range(eventCount):
            bpm = struct.unpack("<f", eventsData[i*4:(i+1)*4])[0]
            if bpm == 0: continue
            log.debug(f"Appended BPM {bpm} at {currMeasure + i / eventCount}")
            bpmObj = O2JBpmObj(bpm=bpm)
            bpmObj.measure = currMeasure + i / eventCount
            bpms.append(bpmObj)

        return bpms

    @staticmethod
    def readEventsNote(eventsData: bytes, column: int, holdBuffer: Dict[int, O2JHoldObj], currMeasure: float) ->\
            List[Union[O2JHitObj, O2JHoldObj]]:
        notes = []

        eventCount = int(len(eventsData) / 4)

        for i in range(eventCount):
            enabled  = struct.unpack("<h", bytes(eventsData[0 + i * 4:2 + i * 4]))[0]
            if enabled == 0: continue

            subMeasure = i / eventCount + currMeasure
            volumePan = struct.unpack("<s", eventsData[2 + i * 4:3 + i * 4])[0]
            volume   = int.from_bytes(volumePan, 'little') // 16
            pan      = int.from_bytes(volumePan, 'little') % 16
            noteType = struct.unpack("<c", eventsData[3 + i * 4:4 + i * 4])[0]
            log.debug(f"Event Data: {eventsData[0 + i * 4:4 + i * 4]}")

            if noteType == O2JConst.HIT_BYTES:
                hit = O2JHitObj(volume=volume, pan=pan, offset=0, column=column)
                hit.measure = subMeasure
                notes.append(hit)
                log.debug(f"Appended Note {column} at {subMeasure}")
            elif noteType == O2JConst.HOLD_HEAD_BYTES:
                hold = O2JHoldObj(volume=volume, pan=pan, column=column, length=-1)
                hold.measure = subMeasure
                holdBuffer[column] = hold
            elif noteType == O2JConst.HOLD_TAIL_BYTES:
                hold = holdBuffer.pop(column)
                hold.tailMeasure = subMeasure
                notes.append(hold)
                log.debug(f"Appended LNote {column} at {subMeasure}, Tail:{hold.tailMeasure}")
            else:
                pass
        return notes
