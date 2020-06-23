#  Copyright (c) 2020 Chris Stranex
#  See LICENSE for licencing information.
#
#  There is NO WARRANTY, to the extent permitted by law.
#
from typing import NamedTuple, Union
import grpc


class InsecurePort(NamedTuple):
    """Creates an insecure port for the grpc server.

    Args:
        host:   The IP address or hostname to listen on
        port:   The port to listen on

    See Also:
        `grpc.Server.add_insecure_port`
    """
    host: str
    port: int

    def __str__(self):
        return f'Insecure Port<{self.host}:{self.port}>'


class SecurePort(NamedTuple):
    """Creates a secure port for the grpc server with the given credentials.

    Args:
        host:   The IP address or hostname to listen on
        port:   The port to listen on
        credentials:    The `grpc.ServerCredentials` to secure the port with

    See Also:
        `grpc.Server.add_secure_port`
    """
    host: str
    port: int
    credentials: grpc.ServerCredentials

    def __str__(self):
        return f'Secure Port<{self.host}:{self.port}>'


Port = Union[SecurePort, InsecurePort]
