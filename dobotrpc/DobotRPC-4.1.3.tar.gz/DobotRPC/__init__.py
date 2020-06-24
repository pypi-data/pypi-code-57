from .NetworkError import NetworkError
from .RPCClient import RPCClient
from .DobotlinkAdapter import DobotlinkAdapter
from .Utils import loggers
from .Magician import MagicianApi
from .M1 import M1Api
from .Lite import LiteApi

magician_api = MagicianApi()
m1_api = M1Api()
lite_api = LiteApi()

__all__ = ("loggers", "RPCClient", "DobotlinkAdapter", "NetworkError",
           "magician_api", "m1_api", "lite_api")
