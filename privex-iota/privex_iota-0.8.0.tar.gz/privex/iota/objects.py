import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Union, List

import pytz
from iota import TransactionHash
from privex.helpers import DictDataClass, DictObject, convert_datetime


@dataclass
class NodeInfo(DictDataClass):
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
    raw_data: Union[dict, DictObject] = field(default_factory=DictObject, repr=False)
    
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


@dataclass
class Neighbor(DictDataClass):
    address: str = ""
    """IP address and port in standard colon format e.g. ``[2a07:e01:3:8a8::1]:15600`` or ``185.130.45.88:15600``"""
    port: int = 0
    domain: str = ""
    """If we connected to this peer via a known domain, contains the domain - otherwise just their IP"""
    alias: str = ""
    """This is a friendly name for a neighbour - generally only set for pre-configured peers in peering.json"""
    connectionType: str = "tcp"
    connected: bool = False
    autopeeringId: str = ""
    
    numberOfAllTransactions: int = 0
    numberOfNewTransactions: int = 0
    numberOfKnownTransactions: int = 0
    numberOfInvalidTransactions: int = 0
    numberOfInvalidRequests: int = 0
    numberOfStaleTransactions: int = 0
    numberOfReceivedTransactionReq: int = 0
    numberOfReceivedMilestoneReq: int = 0
    numberOfReceivedHeartbeats: int = 0
    numberOfSentTransactions: int = 0
    numberOfSentTransactionsReq: int = 0
    numberOfSentMilestoneReq: int = 0
    numberOfSentHeartbeats: int = 0
    numberOfDroppedSentPackets: int = 0
    
    raw_data: Union[dict, DictObject] = field(default_factory=DictObject, repr=False)


Neighbour = Neighbor


@dataclass
class NeighborRes(DictDataClass):
    """Wrapper for response from get_neighbors"""
    neighbors: List[Union[Neighbor, dict]] = field(default_factory=list)
    duration: int = 0
    
    def __post_init__(self):
        # Convert list of neighbor dict's into list of Neighbor objects
        if len(self.neighbors) > 0 and not isinstance(self.neighbors[0], Neighbor):
            self.neighbors = list(Neighbor.from_list(list(self.neighbors)))
    
    @property
    def neighbours(self): return self.neighbors
    
    @neighbours.setter
    def neighbours(self, value): self.neighbors = value


NeighbourRes = NeighborRes

