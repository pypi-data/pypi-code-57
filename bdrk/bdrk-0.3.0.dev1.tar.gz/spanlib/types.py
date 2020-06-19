from enum import Enum


# Should match cluster types expected by helm job image
class ClusterConfigType(str, Enum):
    DUMMY = "dummy"
    GKE = "gke"
    EKS = "eks"


class ModelServerStatus(str, Enum):
    DEPLOYING = "DEPLOYING"
    DEPLOYED = "DEPLOYED"
    STOPPING = "STOPPING"  # aka Undeploying
    STOPPED = "STOPPED"  # aka Not deployed
    FAILED = "FAILED"
    ERROR = "ERROR"
    NEW = "NEW"


class NotebookStatus(str, Enum):
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    FAILED = "FAILED"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"
    ERROR = "ERROR"
    UNKNOWN = "UNKNOWN"
