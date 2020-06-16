"""GRAPHISOFT"""

import argparse
from urllib.request import Request
from urllib.error import URLError
from typing import Optional, List
from .commands import BasicCommands
from .versioning import _Versioning


def create_request(port: int) -> Request:
    """Creates request
    """
    assert port in ACConnection._port_range()
    address = 'http://127.0.0.1:' + str(port)
    req = Request(address)
    req.add_header('Content-Type', 'application/json')
    return req


class ACConnection:
    """Represents a living connection to an existing ARCHICAD instance
    
    Attributes:
        version (:obj:`int`): The version of the current ARCHICAD instance.
        build (:obj:`int`): The build number of the current ARCHICAD instance.
        lang (:obj:`str`): The language code of the current ARCHICAD instance.
        commands: The commands can be called through this object. 
        types: The data types of commands can be access through this object.
        utilities: Some other useful commands can be called through this object. 
    """
    __slots__ = ('port', 'request', 'version', 'build', 'lang', 'commands', 'types', 'utilities')

    def __init__(self, port: int):
        self.port = port
        self.request = create_request(port)
        basic_commands = BasicCommands(self.request)
        self.version, self.build, self.lang = basic_commands.GetProductInfo()
        V = _Versioning(self.version, self.build, self.request)
        self.commands = V.commands
        self.types = V.types
        self.utilities = V.utilities

    @staticmethod
    def connect(port: Optional[int] = None):
        """Tries to connect to a running ARCHICAD instance.
        
        Args:
            port (:obj:`int`, optional): The ARCHICAD's port. If not given, the command line or the default port will be used.
        
        Raises:
            ConnectionError: When the connection is unsuccessful.
        
        Returns:
            :obj:`ACConnection`: The living connection.
        """
        conn: Optional[ACConnection] = None
        if port is not None:
            try:
                conn = ACConnection(port)
                if not conn:
                    raise ConnectionError(f"Could not connect to ARCHICAD on port {port}")
            except URLError:
                pass
        else:
            conn = ACConnection.connect_from_args()
            if not conn:
                port = ACConnection.find_first_port()
                if port:
                    conn = ACConnection.connect(port)
        return conn

    @staticmethod
    def connect_from_args():
        port = ACConnection.port_from_args()
        if not port:
            return None

        return ACConnection.connect(port)

    @staticmethod
    def port_from_args() -> Optional[int]:
        """Tries to extract hostname and port number from command line arguments
        Returns the tuple of the hostame and port number or None
        """
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('--port', type=int, default=None)
        args = parser.parse_args()
        return args.port
        
    @staticmethod
    def _port_range() -> range:
        return range(19723, 19744, 1)

    @staticmethod
    def find_first_port() -> int:
        for port in ACConnection._port_range():
            try:
                ACConnection(port)
                return port
            except Exception:
                continue
        return None

    @staticmethod
    def find_ports(ports: slice) -> List[int]:
        result = []
        for port in ACConnection._port_range():
            try:
                ACConnection(port)
                result.append(port)
            except Exception:
                continue
        return result
