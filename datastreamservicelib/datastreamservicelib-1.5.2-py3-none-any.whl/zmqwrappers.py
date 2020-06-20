"""Implementations for the Abstract Base Classes from datastreamcorelib"""
from typing import cast, Any, Iterable, Dict, Callable, Awaitable  # pylint: disable=W0611
from dataclasses import dataclass, field
import asyncio
import logging

import zmq  # type: ignore  # Get rid of error: Cannot find implementation or library stub for module
import zmq.asyncio  # type: ignore  # Get rid of error: Cannot find implementation or library stub for module

from datastreamcorelib.abstract import ZMQSocket, ZMQSocketType, BaseSocketHandler, ZMQSocketDescription
from datastreamcorelib.pubsub import Subscription, BasePubSubManager, PubSubMessage


LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class Socket(ZMQSocket):
    """Wrapper for the raw AIO socket"""

    socket_type: ZMQSocketType
    _raw_socket: Any = field(default=None, init=False, repr=True)

    def __post_init__(self) -> None:
        """Create the RAW socket"""
        # Map our abstract types to the implementation type
        if self.socket_type == ZMQSocketType.PUB:
            raw_socket_type = zmq.PUB  # pylint: disable=E1101
        if self.socket_type == ZMQSocketType.SUB:
            raw_socket_type = zmq.SUB  # pylint: disable=E1101
        if self.socket_type == ZMQSocketType.REQ:
            raw_socket_type = zmq.REQ  # pylint: disable=E1101
        if self.socket_type == ZMQSocketType.REP:
            raw_socket_type = zmq.REP  # pylint: disable=E1101
        object.__setattr__(self, "_raw_socket", zmq.asyncio.Context.instance().socket(raw_socket_type))

    def subscribe(self, topic: bytes) -> None:
        """Subscribe to a topic"""
        self._raw_socket.subscribe(topic)
        LOGGER.debug("{} subscribed to {!r}".format(self, topic))

    @property
    def closed(self) -> bool:
        """Tells if the socket is open or closed"""
        return bool(self._raw_socket.closed)

    def close(self) -> None:
        """Close the socket"""
        self._raw_socket.close()

    def __getattr__(self, key: str) -> Any:
        """Pass all but our abstractions to the raw socket"""
        return getattr(self._raw_socket, key)

    def __dir__(self) -> Iterable[str]:
        """Expose the raw socket dir too"""
        retval = set(self._raw_socket.__dir__())
        retval.add("__post_init__")
        retval.add("socket_type")
        retval.add("_raw_socket")
        return list(retval)

    def __hash__(self) -> int:
        """Make a hash based on the base sockets one"""
        return int(self._raw_socket.__hash__()) + self.socket_type.value


@dataclass
class SocketHandler(BaseSocketHandler):
    """Implement socket fetching"""

    def get_socket(self, desc: ZMQSocketDescription) -> ZMQSocket:
        """Get socket by address, or bind new one."""
        sock = self._get_cached_socket(desc)
        if sock:
            if not sock.closed:
                return sock
            # Clear the cache and create a new socket.
            del self._sockets_by_desc[desc]

        sock = Socket(desc.sockettype)
        # Bind/connect as needed
        if desc.sockettype not in (ZMQSocketType.SUB, ZMQSocketType.PUB, ZMQSocketType.REQ, ZMQSocketType.REP):
            raise RuntimeError("Don't know how to handle type {}".format(desc.sockettype))
        if desc.sockettype in (ZMQSocketType.SUB, ZMQSocketType.REQ):
            for addr in desc.socketuris:
                sock.connect(addr)
                LOGGER.debug("connected {} to {!r}".format(sock, addr))
        if desc.sockettype in (ZMQSocketType.PUB, ZMQSocketType.REP):
            for addr in desc.socketuris:
                sock.bind(addr)
                LOGGER.debug("bound {} to {!r}".format(sock, addr))

        self._set_cached_socket(desc, sock)
        return sock


@dataclass
class PubSubManager(BasePubSubManager):
    """
Manage subscriptions, sockets and coroutines to read from the sockets
    """

    _socket_reader_tasks: Dict[Socket, "asyncio.Task[Callable[[Socket], Awaitable[None]]]"] = field(
        default_factory=dict, init=False
    )

    def subscribe(self, sub: Subscription) -> None:
        """Add the subscription to our handlers and make sure socket reader is active"""
        super().subscribe(sub)
        sdesc = ZMQSocketDescription(sub.socketuris, ZMQSocketType.SUB)
        sock = cast(Socket, self.sockethandler.get_socket(sdesc))
        if sock not in self._socket_reader_tasks or self._socket_reader_tasks[sock].done():
            # Add the reader task to the mainloop
            self._socket_reader_tasks[sock] = cast(
                "asyncio.Task[Callable[[Socket], Awaitable[None]]]",
                asyncio.get_event_loop().create_task(self._socket_reader(sock)),
            )

    async def _socket_reader(self, sock: Socket) -> None:
        """Waits and dispatches messages as long as the socket is open"""
        while not sock.closed:
            # LOGGER.debug("waiting message on {}".format(sock))
            msgparts = await sock.recv_multipart()
            # LOGGER.debug("got message on {}".format(sock))
            self.raw_zmq_callback(sock, msgparts)

    def _publish_actual(self, msg: PubSubMessage, sock: ZMQSocket) -> None:
        """Implementation for actually handling the send, creates task to the eventloop"""
        sock = cast(Socket, sock)
        sock.send_multipart(msg.zmq_encode())
        # LOGGER.debug("sent {} on {}".format(msg, sock))


def pubsubmanager_factory() -> PubSubManager:
    """Get the default asyncio compatible PubSubManager with proper cast, requiring no arguments"""
    return cast(PubSubManager, PubSubManager.instance(SocketHandler))
