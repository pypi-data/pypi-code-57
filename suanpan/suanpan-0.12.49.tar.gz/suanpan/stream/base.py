# coding=utf-8
from __future__ import absolute_import, print_function

import abc
import os
import traceback
import uuid

import gevent.pywsgi
import geventwebsocket.handler
import socketio
from engineio import static_files

from suanpan import asyncio, error, g, runtime, utils
from suanpan.arguments import Bool, BoolOrInt, Float, Int, String
from suanpan.components import Arguments
from suanpan.interfaces import HasDevMode, HasExitHooks, HasInitHooks, HasLogger
from suanpan.interfaces.optional import HasBaseServices
from suanpan.log import logger
from suanpan.mq import mq
from suanpan.mstorage import mstorage
from suanpan.storage import storage
from suanpan.stream import handlers, loops
from suanpan.stream.interfaces import HasHandlers
from suanpan.stream.objects import Context
from suanpan.utils import functional, json


class Stream(
    HasBaseServices, HasLogger, HasDevMode, HasInitHooks, HasExitHooks, HasHandlers
):
    STREAM_ARGUMENTS = [
        String("stream-recv-queue", default=f"mq-{g.nodeId}"),
        BoolOrInt("stream-recv-queue-block", default=60000),
        Float("stream-recv-queue-delay", default=0),
        Int("stream-recv-queue-max-length", default=1000),
        Bool("stream-recv-queue-trim-immediately", default=False),
        Bool("stream-recv-queue-retry", default=False),
        Int("stream-recv-queue-retry-max-count", default=100),
        Float("stream-recv-queue-retry-timeout", default=1.0),
        Int("stream-recv-queue-retry-max-times", default=3),
        String("stream-send-queue", default="mq-master"),
        Int("stream-send-queue-max-length", default=1000),
        Bool("stream-send-queue-trim-immediately", default=False),
        String("stream-sio-static-folder", default="/dev/shm/web"),
        String("stream-sio-static-url-prefix", default="/"),
    ]
    STREAM_PARAMS_FILE = "params.json"

    def __init__(self):
        super(Stream, self).__init__()
        self.title = ""
        self.argsDict = {}
        self.options = None
        self.args = None

        self.callLoop = StreamCallLoop(self)
        self.triggerLoop = StreamTriggerLoop(self)
        self.sioLoop = StreamSIOLoop(self)

    @property
    def loops(self):
        return [self.callLoop, self.triggerLoop, self.sioLoop]

    def beforeInit(self):
        logger.logDebugInfo()
        logger.debug(f"Stream {self.name} starting...")

    def init(self, *args, **kwargs):
        self.argsDict = self.getArgsDict(*args, **kwargs)
        self.options = self.loadGlobalArguments(self.argsDict)
        self.setBaseServices(self.options)
        self.args = self.loadComponentArguments(self.argsDict)
        return Context.froms(args=self.args)

    def afterInit(self, _):
        self.updateParams(self.loadParams())

    def loadGlobalArguments(self, argsDict=None):
        logger.debug("Loading Global Arguments:")
        argsDict = argsDict or self.argsDict
        args = self.loadFormatArguments(self.getGlobalArguments(), argsDict)
        return Arguments.froms(*args)

    def loadComponentArguments(self, argsDict=None):
        logger.debug("Loading Components Arguments:")
        argsDict = argsDict or self.argsDict
        args = self.loadFormatArguments(self.getComponentArguments(), argsDict)
        return Arguments.froms(*args)

    def getGlobalArguments(self, *args, **kwargs):
        arguments = super(Stream, self).getGlobalArguments(*args, **kwargs)
        return arguments + self.STREAM_ARGUMENTS

    def getParams(self):
        return {arg.paramName: self.args.get(arg.paramName) for arg in self.ARGUMENTS}

    def updateParams(self, params):
        for key, value in params.items():
            arg = self.paramsArgsMap.get(key)
            if arg and value is not None:
                self.args.update({key: value for key in (arg.key, arg.alias) if key})
        return self.getParams()

    def loadParams(self):
        logger.debug(f"Loading params from {self.paramsFilePath}")
        try:
            storage.download(self.paramsFileKey, self.paramsFilePath)
            params = json.load(self.paramsFilePath)
            logger.debug(f"Loaded params: {params}")
            return params
        except Exception:  # pylint: disable=broad-except
            tracebackInfo = traceback.format_exc()
            logger.debug(f"Load params error: {tracebackInfo}")
            return {}

    def saveParams(self, params):
        logger.debug(f"Saving params: {self.paramsFilePath}")
        json.dump(params, self.paramsFilePath)
        storage.upload(self.paramsFileKey, self.paramsFilePath)
        return params

    @functional.lazyproperty
    def paramsArgsMap(self):
        argsmap = {}
        for arg in self.ARGUMENTS:
            if arg.key:
                argsmap[arg.key] = arg
            if arg.alias:
                argsmap[arg.alias] = arg
        return argsmap

    @functional.lazyproperty
    def paramsFileKey(self):
        return storage.getKeyInNodeConfigsStore(self.STREAM_PARAMS_FILE)

    @functional.lazyproperty
    def paramsFilePath(self):
        return storage.getPathInNodeConfigsStore(self.STREAM_PARAMS_FILE)

    @runtime.globalrun
    def start(self, *args, **kwargs):
        self.callBeforeInitHooks()
        context = self.init(*args, **kwargs)
        self.callAfterInitHooks(context)
        self.registerBeforeExitHooks(context)
        self.run()

    def run(self):
        runners = (loop.start for loop in self.loops if loop.ready)
        asyncio.wait(asyncio.run(runners))

    @property
    def vars(self):
        return mstorage.vars


class StreamBaseLoop(HasHandlers):
    __metaclass__ = abc.ABCMeta

    DEFAULT_HANDLER_KEY = None
    DEFAULT_HANDLER_CLASS = handlers.Handler
    DEFAULT_LOGGER_MAX_LENGTH = 120
    DEFAULT_MESSAGE = {}

    def __init__(self, stream):
        super(StreamBaseLoop, self).__init__()
        self.stream = stream

    @property
    def ready(self):
        return self.hasHandler(self.DEFAULT_HANDLER_KEY)

    def getHandler(self, key):
        if not self.hasHandler(key):
            super(StreamBaseLoop, self).setHandler(key, self.DEFAULT_HANDLER_CLASS())
        return super(StreamBaseLoop, self).getHandler(key)

    def generateRequestId(self):
        return uuid.uuid4().hex

    def generateMessage(self, **kwargs):
        message = {}
        message.update(self.DEFAULT_MESSAGE, **kwargs)
        message["id"] = self.generateRequestId()
        return message

    @abc.abstractmethod
    def start(self):
        pass


class StreamMQBaseLoop(StreamBaseLoop):
    def _send(self, message, data, queue=None):
        queue = queue or self.stream.options["stream-send-queue"]
        data = {
            "node_id": g.nodeId,
            "request_id": message["id"],
            **data,
        }
        logger.debug(
            utils.shorten(f"Send to `{queue}`: {data}", self.DEFAULT_LOGGER_MAX_LENGTH)
        )
        return mq.sendMessage(
            queue,
            data,
            maxlen=self.stream.options["stream-send-queue-max-length"],
            trimImmediately=self.stream.options["stream-send-queue-trim-immediately"],
        )

    def sendSuccessMessage(self, message, data, queue=None):
        if not all(key.startswith("out") for key in data):
            raise error.StreamError(
                "Success Message data only accept keys starts with 'out'"
            )
        data = {key: value for key, value in data.items() if value is not None}
        data.update(success="true")
        return self._send(message, data, queue=queue)

    def sendFailureMessage(self, message, msg, queue=None):
        if not isinstance(msg, str):
            raise error.StreamError("Failure Message msg only accept string")
        data = {"msg": msg, "success": "false"}
        return self._send(message, data, queue=queue)

    def send(self, results, queue=None, message=None, args=None, **_):
        message = message or self.generateMessage()
        outputs = self.getHandler().save(results, args=args, message=message)
        if outputs:
            self.sendSuccessMessage(message, outputs, queue=queue)

    def sendError(self, msg, queue=None, message=None):
        message = message or self.generateMessage()
        return self.sendFailureMessage(message, msg, queue=queue)

    def sendMissionMessage(self, message, data, queue=None):
        if not all(key.startswith("in") for key in data):
            raise error.StreamError(
                "Mission Message data only accept keys starts with 'in'"
            )
        data = {key: value for key, value in data.items() if value is not None}
        data.update(id=message["id"])
        return self._send(message, data, queue=queue)

    def getHandler(self):
        if not self.hasHandler(self.DEFAULT_HANDLER_KEY):
            self.setHandler(self.DEFAULT_HANDLER_CLASS())
        return super(StreamMQBaseLoop, self).getHandler(self.DEFAULT_HANDLER_KEY)

    def setHandler(self, handler):
        return super(StreamMQBaseLoop, self).setHandler(
            self.DEFAULT_HANDLER_KEY, handler
        )

    def handle(self, message, *args, **kwargs):
        title = f"{message['id']} - {self.DEFAULT_HANDLER_KEY}"
        _run = runtime.costrun(title)(self.getHandler().run)

        try:
            outputs = _run(self.stream, message, *args, **kwargs)
            if outputs:
                self.sendSuccessMessage(message, outputs)
        except Exception as e:  # pylint: disable=broad-except
            tracebackInfo = traceback.format_exc()
            logger.error(tracebackInfo)
            self.sendFailureMessage(message, tracebackInfo)
            self.stream.sioLoop.notifyError(e)


class StreamCallLoop(StreamMQBaseLoop):
    DEFAULT_HANDLER_KEY = "call"
    DEFAULT_HANDLER_CLASS = handlers.CallHandler

    def __init__(self, *args, **kwargs):
        super(StreamCallLoop, self).__init__(*args, **kwargs)
        self.lastMessage = None

    def subscribe(self, **kwargs):
        return mq.subscribeQueue(
            self.stream.options["stream-recv-queue"],
            group=g.nodeGroup,
            consumer=g.nodeId,
            block=self.stream.options["stream-recv-queue-block"],
            delay=self.stream.options["stream-recv-queue-delay"],
            **kwargs,
        )

    def retryPendingMessages(self, **kwargs):
        return mq.retryPendingMessages(
            self.stream.options["stream-recv-queue"],
            group=g.nodeGroup,
            consumer=g.nodeId,
            count=self.stream.options["stream-recv-queue-retry-max-count"],
            maxTimes=self.stream.options["stream-recv-queue-retry-max-times"],
            timeout=self.stream.options["stream-recv-queue-retry-timeout"],
            maxlen=self.stream.options["stream-recv-queue-max-length"],
            trimImmediately=self.stream.options["stream-recv-queue-trim-immediately"],
            **kwargs,
        )

    def retryLastMessage(self):
        if not self.lastMessage:
            logger.debug("Stream Call Loop No Message To Retry")
            return

        self._send(
            self.lastMessage,
            self.lastMessage,
            queue=self.stream.options["stream-recv-queue"],
        )

    @runtime.globalrun
    def start(self):
        logger.debug("Stream Call Loop Starting...")
        if self.stream.options["stream-recv-queue-retry"]:
            self.retryPendingMessages()
        for message in self.subscribe():
            self.lastMessage = message.get("data", {})
            self.handle(self.lastMessage)


class StreamTriggerLoop(StreamMQBaseLoop):
    DEFAULT_HANDLER_KEY = "trigger"
    DEFAULT_HANDLER_CLASS = handlers.TriggerHandler
    DEFAULT_LOOP = loops.Interval(1)

    def __init__(self, stream, loop=None):
        super(StreamTriggerLoop, self).__init__(stream)
        self._loop = loop or self.DEFAULT_LOOP

    def _list(self, data):
        if isinstance(data, (tuple, list)):
            return data
        if data is None:
            return []
        return [data]

    def loop(self, funcOrIter, *_, **__):
        self._loop = funcOrIter if callable(funcOrIter) else lambda: funcOrIter

    @runtime.globalrun
    def start(self):
        logger.debug("Stream Trigger Loop Starting...")
        for data in self._loop():
            self.handle(self.generateMessage(), *self._list(data))


class StreamSIOLoop(StreamBaseLoop):
    DEFAULT_HANDLER_CLASS = handlers.SIOHandler
    EVENT_CONNECT = "connect"
    EXTRA_CONTEXT_TYPES = {"mjs": "text/javascript"}

    def __init__(self, stream):
        super(StreamSIOLoop, self).__init__(stream)
        self.sio = socketio.Server(async_mode="gevent", cors_allowed_origins="*")
        self.options = self._getDefaultOptions()
        self._enabled = True

    def _getDefaultOptions(self):
        options = Context()
        return options

    @functional.lazyproperty
    def staticFolder(self):
        return self.stream.options["stream-sio-static-folder"]

    @functional.lazyproperty
    def staticUrlPrefix(self):
        return self.getFullUrlPrefix(
            self.stream.options["stream-sio-static-url-prefix"]
        )

    @property
    def contentTypes(self):
        return static_files.content_types

    @property
    def ready(self):
        return self._enabled or g.debug

    def enable(self):
        self._enabled = True
        return self

    def disable(self):
        self._enabled = False
        return self

    def getHandler(self, key):
        initial = not self.hasHandler(key)
        handler = super(StreamSIOLoop, self).getHandler(key)
        if initial:
            self.sio.on(key)(self._handle(key, handler))
        return handler

    def setHandler(self, key, handler):
        return self.getHandler(key).use(handler)

    def _handle(self, key, handler):
        def _dec(sid, data):
            title = f"{sid} - sio:{key}"
            _run = runtime.costrun(title)(handler.run)
            try:
                result = _run(self.stream, data, sid)
                return {"success": True, "data": result}
            except Exception as e:  # pylint: disable=broad-except
                logger.error(traceback.format_exc())
                return {"success": False, "error": self._formatError(e)}

        return _dec

    def getStaticFiles(self, folder):
        self.contentTypes.update(self.EXTRA_CONTEXT_TYPES)
        folder = self.getFullUrlPrefix(os.path.abspath(folder))
        prefixUrl = self.getFullUrlPrefix(self.staticUrlPrefix)
        return {prefixUrl: folder}

    def getFullUrlPrefix(self, prefix):
        return prefix.rstrip("/") + "/"

    def emit(self, *args, **kwargs):
        if self.ready:
            self.sio.emit(*args, **kwargs)

    def enter(self, *args, **kwargs):
        self.sio.enter_room(*args, **kwargs)

    def leave(self, *args, **kwargs):
        self.sio.leave_room(*args, **kwargs)

    def notifyError(self, err, *args, **kwargs):
        self.emit("errors.notify", {"error": self._formatError(err)}, *args, **kwargs)

    def _formatError(self, err):
        return {
            "message": str(err),
            "trackback": traceback.format_exc(),
        }

    @runtime.globalrun
    def start(self):
        logger.debug("Stream SIO Loop Starting...")
        staticFiles = self.getStaticFiles(self.staticFolder)
        app = socketio.WSGIApp(self.sio, static_files=staticFiles)
        gevent.pywsgi.WSGIServer(
            ("", 8888), app, handler_class=geventwebsocket.handler.WebSocketHandler
        ).serve_forever()
