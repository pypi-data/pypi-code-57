"""Baseclasses for services using asyncio as eventloop"""
from typing import Union, MutableMapping, Any, Optional
from pathlib import Path
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import tempfile
import logging

import signal as posixsignal
import asyncio
import toml

from datastreamcorelib.abstract import ZMQSocketType, ZMQSocketDescription
from datastreamcorelib.utils import create_heartbeat_message


from .zmqwrappers import PubSubManager, pubsubmanager_factory

LOGGER = logging.getLogger(__name__)
EXCEPTION_EXITCODE = 200


# See https://github.com/python/mypy/issues/5374 why the typing ignore
@dataclass  # type: ignore
class BaseService(ABC):
    """Baseclass for services using asyncio as eventloop"""

    _exitcode: Union[None, int] = field(init=False, default=None)
    _quitevent: asyncio.Event = field(init=False, default_factory=asyncio.Event, repr=False)

    @abstractmethod
    async def setup(self) -> None:
        """Called once by the run method before wating for exitcode to be set"""
        raise NotImplementedError()

    @abstractmethod
    async def teardown(self) -> None:
        """Called once by the run method before exiting"""
        raise NotImplementedError()

    @abstractmethod
    def reload(self) -> None:
        """Called whenever the service is told to reload (usually via SIGHUP), setup might want to call this"""
        raise NotImplementedError()

    def quit(self, exitcode: int = 0) -> None:
        """set the exitcode which as side-effect will tell the run method to do teardown and finally exit"""
        LOGGER.debug("called with code={}".format(exitcode))
        self._exitcode = exitcode
        self._quitevent.set()

    def hook_signals(self) -> None:
        """Hook handlers for signals and the default exception handler"""
        loop = asyncio.get_event_loop()
        loop.set_exception_handler(self.default_exception_handler)
        loop.add_signal_handler(posixsignal.SIGINT, self.quit)
        loop.add_signal_handler(posixsignal.SIGTERM, self.quit)
        try:
            loop.add_signal_handler(posixsignal.SIGHUP, self.reload)
        except AttributeError:
            # Windows does not implement all signals
            pass

    def default_exception_handler(self, loop: asyncio.AbstractEventLoop, context: MutableMapping[str, Any]) -> None:
        """Default exception handler, logs the exception and quits (forcefully)"""
        msg = context.get("exception", context["message"])
        if isinstance(msg, Exception):
            LOGGER.exception("Unhandled in loop {}".format(loop), exc_info=msg)
        else:
            LOGGER.error("Called with context message {} in loop {}".format(msg, loop))
        # Make sure we get killed if quit hangs...
        BaseService.set_exit_alarm()
        # Call quit with the defined exit code
        self.quit(EXCEPTION_EXITCODE)

    @classmethod
    def set_exit_alarm(cls, timeout: int = 2) -> bool:
        """Clears handlers from alarm and sets an alarm signal for hard exit on timeout

        returns False if alarm could not be set. Yes, it can only take full integer seconds"""
        try:
            # Try to make sure alarm is not handled and set alarm to make sure teardown doesn't hang
            loop = asyncio.get_event_loop()
            loop.remove_signal_handler(posixsignal.SIGALRM)
            posixsignal.signal(posixsignal.SIGALRM, posixsignal.SIG_DFL)
            posixsignal.alarm(timeout)
            return True
        except AttributeError:
            # Windows does not implement all signals
            return False

    @classmethod
    def clear_exit_alarm(cls) -> bool:
        """Clear pending alarm"""
        try:
            posixsignal.signal(posixsignal.SIGALRM, posixsignal.SIG_DFL)
            posixsignal.alarm(0)
            return True
        except AttributeError:
            # Windows does not implement all signals
            return False

    async def run(self) -> int:
        """Main entrypoint, should be called with asyncio.get_event_loop().run_until_complete()"""
        await self.setup()
        await self._quitevent.wait()
        if self._exitcode is None:
            LOGGER.error("Got quitevent but exitcode is not set")
            self._exitcode = 1
        # Try to make sure teardown does not hang
        BaseService.set_exit_alarm()
        await self.teardown()
        return self._exitcode


@dataclass
class SimpleServiceMixin:
    """Mixin for a bit of automagics for heartbeats, config loading etc"""

    configpath: Path
    psmgr: PubSubManager = field(init=False, default_factory=pubsubmanager_factory)
    config: MutableMapping[str, Any] = field(init=False, default_factory=dict)
    _hbtask: Optional["asyncio.Task[Any]"] = field(init=False, default=None)

    async def _heartbeat_task(self) -> None:
        """Send a periodic heartbeat"""
        while True:
            self.psmgr.publish(create_heartbeat_message())
            await asyncio.sleep(1)

    def _resolve_default_pub_socket(self) -> None:
        """Resolves the path for default PUB socket and sets it to PubSubManager"""
        pub_default = "ipc://" + str(Path(tempfile.gettempdir()) / self.configpath.name.replace(".toml", "_pub.sock"))
        if "zmq" in self.config and "pub_sockets" in self.config["zmq"]:
            pub_default = self.config["zmq"]["pub_sockets"]
        sdesc = ZMQSocketDescription(pub_default, ZMQSocketType.PUB)
        LOGGER.debug("sdesc={}".format(sdesc))
        sock = self.psmgr.sockethandler.get_socket(sdesc)
        self.psmgr.default_pub_socket = sock

    def stop_hbtask_graceful(self) -> None:
        """Stops the hb task if it's active"""
        if not self._hbtask:
            return
        if self._hbtask.done():
            self._hbtask = None
            return
        self._hbtask.cancel()
        self._hbtask = None

    def reload(self) -> None:
        """Load configs, restart sockets"""
        self.psmgr.sockethandler.close_all_sockets()
        with self.configpath.open("rt", encoding="utf-8") as filepntr:
            self.config = toml.load(filepntr)
        self._resolve_default_pub_socket()
        self.stop_hbtask_graceful()
        self._hbtask = asyncio.get_event_loop().create_task(self._heartbeat_task())

    async def teardown(self) -> None:
        """Close all sockets"""
        self.stop_hbtask_graceful()
        self.psmgr.sockethandler.close_all_sockets()


@dataclass
class SimpleService(SimpleServiceMixin, BaseService):
    """Simple service does a bit of automagics in setup"""

    async def setup(self) -> None:
        """Called once by run, just calls reload which loads our config"""
        self.hook_signals()
        self.reload()
