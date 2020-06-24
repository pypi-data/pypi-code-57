import asyncio
import io
import struct
from collections import defaultdict
from typing import Optional

from medusa_protocol import BinaryResponse, BinaryRequest


class TcpClient:
    """
    Client for TCP Call
    """
    PROTOCOL = struct.Struct(">I")

    def __init__(self, reader: asyncio.StreamReader,
                 writer: asyncio.StreamWriter):
        self.reader = reader
        self.writer = writer
        self.serial = 0
        self.futures = {}
        self.loop = asyncio.get_event_loop()
        self.reader_task = self.loop.create_task(self._response_reader())

    async def _response_reader(self):
        try:
            while True:
                body_size = self.PROTOCOL.unpack(
                    await self.reader.readexactly(self.PROTOCOL.size)
                )[0]
                body_bytes = await self.reader.readexactly(body_size)
                response = BinaryResponse()
                response.decode(body_bytes)
                future = self.futures.pop(response.id, None)
                if future is None:
                    continue
                if 400 == response.code or 500 == response.code:
                    future.set_exception(Exception())
                    continue

                future.set_result(response)
        finally:
            while self.futures:
                _, future = self.futures.popitem()

                if future.done():
                    continue

                future.set_exception(ConnectionAbortedError)

    async def close(self):
        self.writer.write(self.PROTOCOL.pack(0))
        self.reader_task.cancel()
        await asyncio.gather(self.reader_task, return_exceptions=True)
        self.loop.call_soon(self.writer.close)
        self.writer.write_eof()
        self.writer.close()

    def send(self, request: BinaryRequest, **kwargs):
        self.serial = request.id
        self.futures[self.serial] = self.loop.create_future()
        with io.BytesIO() as f:
            body = request.encode()
            f.write(self.PROTOCOL.pack(len(body)))
            f.write(body)
            self.writer.write(f.getvalue())
        return self.futures[self.serial]


class UdpClient(asyncio.BaseProtocol):
    def __init__(self, loop: asyncio.AbstractEventLoop = None):
        self.loop = loop or asyncio.get_event_loop()
        self.closing = self.loop.create_future()
        self.transport = None
        self.last_id = 1
        self.waiting = defaultdict(dict)

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data: bytes, addr):
        response: BinaryResponse = BinaryResponse()
        response.decode(data)
        future = self.waiting[addr[:2]][response.id]
        future.set_result(response)

    def send(self, addr, request: BinaryRequest):
        future = self.loop.create_future()
        self.waiting[addr][request.id] = future
        self.transport.sendto(request.encode(), addr)
        return future

    def connection_lost(self, exc: Optional[Exception]) -> None:
        self.closing.set_exception(exc)
