import struct

from aiomisc.service import UDPServer
from medusa_protocol import BinaryRequest, BinaryResponse

from .Router import Router
from .Exceptions import RouterException


class UdpServer(UDPServer):
    __required__ = 'router',
    PROTOCOL = struct.Struct(">I")
    router: Router

    async def handle_datagram(self, data: bytes, addr):
        request: BinaryRequest = BinaryRequest()
        request.decode(data)
        try:
            callback = self.router.get(request.action)
            response: BinaryResponse = callback(request)
        except RouterException as e:
            response: BinaryResponse = BinaryResponse()
            response.id = request.id
            response.code = 404
            response.body = "Doesn't exist"
        self.sendto(response.encode(), addr)
