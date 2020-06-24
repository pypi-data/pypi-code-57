"""
Copyright::

    +===================================================+
    |                 © 2020 Privex Inc.                |
    |               https://www.privex.io               |
    +===================================================+
    |                                                   |
    |        Privex's Random IOTA Tools                 |
    |        License: X11/MIT                           |
    |                                                   |
    |        Core Developer(s):                         |
    |                                                   |
    |          (+)  Chris (@someguy123) [Privex]        |
    |                                                   |
    +===================================================+

    Privex's Random IOTA Tools
    Copyright (c) 2020    Privex Inc. ( https://www.privex.io )

"""

import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Union

import pytz
from iota import Iota, TransactionHash
from privex.helpers import convert_datetime, DictDataClass

__all__ = [
    'IOTANodeInfo', 'PrivexIota'
]


@dataclass
class IOTANodeInfo(DictDataClass):
    latestMilestone: str = None
    latestSolidSubtangleMilestone: str = None
    appVersion: str = "0.0.0"
    coordinatorAddress: str = None
    duration: Union[int, float] = 0
    features: List[str] = field(default_factory=list)
    lastSnapshottedMilestoneIndex: int = None
    latestMilestoneIndex: int = None
    latestSolidSubtangleMilestoneIndex: int = None
    milestoneStartIndex: int = None
    isSynced: bool = False
    appName: str = "HORNET"
    neighbors: int = 0
    time: int = None
    tips: int = 0
    transactionsToRequest: int = 0
    raw_data: dict = field(default_factory=dict, repr=False)
    
    def __post_init__(self):
        if isinstance(self.latestMilestone, TransactionHash):
            self.latestMilestone = str(self.latestMilestone)
        if isinstance(self.latestSolidSubtangleMilestone, TransactionHash):
            self.latestSolidSubtangleMilestone = str(self.latestSolidSubtangleMilestone)
    
    @property
    def time_date(self) -> datetime:
        return convert_datetime(self.time / 1000) if isinstance(self.time, int) else convert_datetime(self.time)
    
    @property
    def time_behind(self) -> timedelta:
        return datetime.utcnow().replace(tzinfo=pytz.UTC) - self.time_date.replace(tzinfo=pytz.UTC)
    
    @property
    def as_json(self) -> str:
        return json.dumps(dict(self), indent=4)


class PrivexIota(Iota):
    def get_node_info(self) -> IOTANodeInfo:
        info = super(PrivexIota, self).get_node_info()
        return IOTANodeInfo.from_dict(info)

