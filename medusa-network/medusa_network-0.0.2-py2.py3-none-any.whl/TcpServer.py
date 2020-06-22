import asyncio
import logging
import struct
import io

from aiomisc.service import TCPServer
from medusa_protocol.binary.BinaryRequest import BinaryRequest
from medusa_protocol.binary.BinaryResponse import BinaryResponse

from .Exceptions import RouterException, TCPServerException
from .Router import Router


class TcpServer(TCPServer):
    __required__ = 'router',
    PROTOCOL = struct.Struct(">I")
    router: Router

    async def handle_client(
        self, reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter
    ):
        """
        this method is called every time the Server receive and call from a client
        is an async method and if the request is a @BinaryRequest get the action and call the @Router attribute
        execute the callback funtion and return a @BinaryResponse
        :param reader:
        :param writer:
        :return:
        """
        try:
            while True:
                body_size = self.PROTOCOL.unpack(
                    await reader.readexactly(self.PROTOCOL.size)
                )[0]
                if body_size == 0:
                    logging.info('Client tcp://%s:%d initial to close connection',
                             *writer.get_extra_info('peername')[:2])
                    return
                body_bytes = await reader.readexactly(body_size)
                request: BinaryRequest = BinaryRequest()
                request.decode(body_bytes)
                try:
                    callback = self.router.get(request.action)
                    response: BinaryResponse = callback(request)
                    response.id = request.id
                except RouterException as e:
                    response: BinaryResponse = BinaryResponse()
                    response.id = request.id
                    response.code = 404
                    response.body = "Doesn't exist"
                with io.BytesIO() as f:
                    f.write(self.PROTOCOL.pack(len(response.encode())))
                    f.write(response.encode())
                    payload = f.getvalue()
                writer.write(payload)
        except TCPServerException:
            writer.close()
            raise

