# -*- coding: utf-8 -*-
# Copyright (c) 2016 - 2020 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
""" Instrumentation helper responsible for adding dynamic callback
"""
import logging

from ..remote_exception import RemoteException
from ..utils import HAS_ASYNCIO
from .import_hook import ModuleFinder
from .strategies import (
    DBApi2Strategy,
    DjangoStrategy,
    FlaskStrategy,
    ImportHookStrategy,
    LXMLResolverStrategy,
    Psycopg2Strategy,
    PyramidStrategy,
    WSGIFactoryStrategy,
    WSGIReceiverStrategy,
    WSGIStrategy,
)

STRATEGIES = {
    "import_hook": ImportHookStrategy,
    "DBApi2": DBApi2Strategy,
    "django": DjangoStrategy,
    "psycopg2": Psycopg2Strategy,
    "flask": FlaskStrategy,
    "pyramid": PyramidStrategy,
    "wsgi": WSGIStrategy,
    "wsgi_factory": WSGIFactoryStrategy,
    "wsgi_receiver": WSGIReceiverStrategy,
    "lxml_resolver": LXMLResolverStrategy,
}

if HAS_ASYNCIO:
    from .strategies import (
        AioHTTPHookStrategy,
        AioHTTPInstallStrategy,
        AsyncEventLoopStrategy,
        AsyncImportHookStrategy,
    )

    STRATEGIES.update({
        "async_event_loop": AsyncEventLoopStrategy,
        "async_import_hook": AsyncImportHookStrategy,
        "aiohttp_install": AioHTTPInstallStrategy,
        "aiohttp_hook": AioHTTPHookStrategy,
    })

LOGGER = logging.getLogger(__name__)


class Instrumentation(object):
    """ The instrumentation class is the exposed face of the
    instrumentation engine. It dispatchs to the right strategy,
    the default one is set_attr.

    The instrumentation class takes attack queue and observation queue as parameters.

    The instrument class dispatch to different strategies based on strategy
    name defined in callback. It ask stategy for an unique id based on hook path
    infos and ensure to have only one strategy instance per id. It's needed
    for DBApi2 strategy where every sqlite3 callbacks will be stored in the same
    strategy to avoid double-instrumentation.

    It also instantiate a global ImportHook that strategy will register
    against when hooking.

    TODO:
        - Store callbacks in a single callback tree
        - Transform the remaining strategies into stateless patchers
    """

    def __init__(self, observation_queue, queue, before_hook_point=None):
        self.observation_queue = observation_queue
        self.queue = queue
        self.strategies = {}
        self.before_hook_point = before_hook_point
        self.import_hook = ModuleFinder()
        self.enabled = False

    def add_callback(self, callback):
        """ Add a callback. The callback defines itself where it should
        hook to and the strategy use for hooking (set_attr or DBApi2)
        """
        try:
            strategy_class = self._get_strategy_class(callback.strategy)

            # Get the strategy id
            strategy_id = strategy_class.get_strategy_id(callback)

            # Check if we already have a strategy
            if strategy_id in self.strategies:
                strategy_instance = self.strategies[strategy_id]
                LOGGER.debug(
                    "Reusing strategy %s for id %s",
                    strategy_instance,
                    strategy_id,
                )
            else:
                strategy_instance = strategy_class(
                    strategy_id,
                    self.observation_queue,
                    self.queue,
                    self.import_hook,
                    self.before_hook_point,
                )
                LOGGER.debug(
                    "Instantiate strategy %s for id %s -> %s",
                    strategy_class,
                    strategy_id,
                    strategy_instance,
                )
                self.strategies[strategy_id] = strategy_instance

            strategy_instance.add_callback(callback)
        except Exception:
            # If the strategy fails to hook either at instantiation
            # or hook method, catch the exception and log it
            LOGGER.exception(
                "Callback %r fails to hook", callback, exc_info=True
            )

            # And send the exception back to the backend
            infos = {"callback": callback.__dict__}
            remote_exception = RemoteException.from_exc_info(callback_payload=infos)
            self.queue.put(remote_exception)

    def deinstrument(self, callback):
        """ Deactive instrumentation on the callback endpoint
        """
        strategy_class = self._get_strategy_class(callback.strategy)

        # Get the strategy id
        strategy_id = strategy_class.get_strategy_id(callback)

        self.strategies[strategy_id].deinstrument(callback)

    def deinstrument_all(self):
        """ Deactive instrumentation on all callbacks by calling
        deinstrument_all on all strategies
        """
        for strategy in self.strategies.values():
            strategy.deinstrument_all()
        self.enabled = False

    def hook_all(self):
        """ First, inject the import hook in sys.meta if not present.
        Then hook all strategies, must be called after all the callbacks has
        been added. The call to strategies.hook will register patcher
        to the actual hook.
        Then call import_hook.apply_patchers that will apply patcher on
        modules already imported.
        """
        self.import_hook.inject()
        for strategy in self.strategies.values():
            strategy.hook()
        self.import_hook.apply_patchers()
        self.enabled = True

    @staticmethod
    def _get_strategy_class(strategy):
        """ Return a strategy class depending on the strategy name passed
        in parameter.
        Raise a NotImplementedError if the strategy is unknown.
        """
        strategy_cls = STRATEGIES.get(strategy)
        if strategy_cls is None:
            raise NotImplementedError(
                "Unknown hooking strategy {!r}".format(strategy))
        return strategy_cls
