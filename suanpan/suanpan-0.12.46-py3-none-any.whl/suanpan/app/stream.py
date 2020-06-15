# coding=utf-8
from __future__ import absolute_import, print_function

import os

from suanpan import error
from suanpan.app import loops
from suanpan.app.base import BaseApp
from suanpan.app.modules import modules
from suanpan.model.arguments import HotReloadModel
from suanpan.stream import Stream
from suanpan.utils import functional

COMPONENT_ARGUMENT_CLASSES = (HotReloadModel,)


class BaseStreamApp(BaseApp):
    def __call__(self, funcOrApp):
        if not isinstance(funcOrApp, BaseApp):
            self._handler.use(functional.instancemethod(funcOrApp))
        return self

    @property
    def name(self):
        return self._stream.name

    @functional.lazyproperty
    def _stream(self):
        raise NotImplementedError("Method not implemented!")

    @functional.lazyproperty
    def _loop(self):
        raise NotImplementedError("Method not implemented!")

    @functional.lazyproperty
    def _handler(self):
        return self._loop.getHandler()

    def bootstrap(self):
        self.modules.info()

    def start(self, *args, **kwargs):
        self.bootstrap()
        super(BaseStreamApp, self).start(*args, **kwargs)
        return self._stream.start(*args, **kwargs)

    def input(self, argument):
        if isinstance(argument, COMPONENT_ARGUMENT_CLASSES):
            self._stream.ARGUMENTS.append(argument)
        else:
            self._handler.input(argument)
        return self

    def output(self, argument):
        if isinstance(argument, HotReloadModel):
            raise error.AppError(f"{argument.name} can't be set as output!")
        self._handler.output(argument)
        return self

    def param(self, argument):
        self._stream.ARGUMENTS.append(argument)
        return self

    def column(self, argument):
        self._stream.ARGUMENTS.append(argument)
        return self

    def beforeInit(self, hook):
        self._stream.addBeforeInitHooks(hook)
        return hook

    def afterInit(self, hook):
        self._stream.addAfterInitHooks(hook)
        return hook

    def beforeCall(self, hook):
        self._handler.addBeforeCallHooks(hook)
        return hook

    def afterCall(self, hook):
        self._handler.addAfterCallHooks(hook)
        return hook

    def beforeExit(self, hook):
        self._stream.addBeforeExitHooks(hook)
        return hook

    def load(self, *args, **kwargs):
        return self._handler.load(*args, **kwargs)

    def send(self, *args, **kwargs):
        return self._loop.send(*args, **kwargs)

    def save(self, *args, **kwargs):
        return self.send(*args, **kwargs)

    @property
    def modules(self):
        return modules


class StreamApp(BaseStreamApp):
    @functional.lazyproperty
    def _stream(self):
        return Stream()

    @functional.lazyproperty
    def _loop(self):
        return self._stream.callLoop

    @property
    def args(self):
        return self._stream.args

    @property
    def vars(self):
        return self._stream.vars

    @functional.lazyproperty
    def trigger(self):  # pylint: disable=invalid-overridden-method
        return TriggerApp(self._stream)

    @functional.lazyproperty
    def sio(self):
        return SIOAppManager(self._stream)

    def title(self, title):
        self._stream.title = title
        return self

    def bootstrap(self):
        super(StreamApp, self).bootstrap()
        self.trigger.bootstrap(self)
        self.sio.bootstrap(self)


class TriggerApp(BaseStreamApp):
    def __init__(self, stream, *args, **kwargs):
        super(TriggerApp, self).__init__(*args, **kwargs)
        self.__stream = stream

    @functional.lazyproperty
    def _stream(self):
        return self.__stream

    @functional.lazyproperty
    def _loop(self):
        return self._stream.triggerLoop

    def interval(self, seconds, *args, **kwargs):
        self._loop.loop(loops.Interval(seconds, *args, **kwargs))
        return self

    def loop(self, funcOrIter, *args, **kwargs):
        self._loop.loop(funcOrIter, *args, **kwargs)
        return self

    def title(self, title):
        self._stream.title = title
        return self

    def bootstrap(self, app):
        pass


class SIOAppManager(object):
    def __init__(self, stream, *args, **kwargs):
        super(SIOAppManager, self).__init__(*args, **kwargs)
        self.__stream = stream
        self._siomap = {}

    def __call__(self, event):
        if event not in self._siomap:
            self._siomap[event] = SIOApp(self._stream, event)
        return self._siomap[event]

    @functional.lazyproperty
    def _stream(self):
        return self.__stream

    @functional.lazyproperty
    def _loop(self):
        return self._stream.sioLoop

    def title(self, title):
        self._loop.options.params.configs.title = title
        return self

    def params(self, params):
        self._loop.options.params.configs.params = params
        return self

    def emit(self, *args, **kwargs):
        self._loop.emit(*args, **kwargs)
    
    def enter(self, *args, **kwargs):
        return self._loop.enter(*args, **kwargs)

    def leave(self, *args, **kwargs):
        return self._loop.leave(*args, **kwargs)

    def error(self, err, *args, **kwargs):
        self._loop.notifyError(err, *args, **kwargs)

    def static(self, *paths):
        return os.path.join(self._loop.staticFolder, *paths)

    def enable(self):
        self._loop.enable()
        return self

    def disable(self):
        self._loop.disable()
        return self

    def _handle(self, event, handlers):
        def _func(context):
            result = None
            for handler in handlers:
                result = handler(context)
            return result

        _func.__name__ = event
        return _func

    def bootstrap(self, app):
        for event, handlers in app.modules.handlers.items():
            self(event)(self._handle(event, handlers))


class SIOApp(BaseStreamApp):
    def __init__(self, stream, event, *args, **kwargs):
        super(SIOApp, self).__init__(*args, **kwargs)
        self.__stream = stream
        self._event = event

    @functional.lazyproperty
    def _stream(self):
        return self.__stream

    @functional.lazyproperty
    def _loop(self):
        return self._stream.sioLoop

    @functional.lazyproperty
    def _handler(self):
        return self._loop.getHandler(self._event)

    def emit(self, *args, **kwargs):
        return self._loop.emit(*args, **kwargs)

    @property
    def contentTypes(self):
        return self._loop.contentTypes
