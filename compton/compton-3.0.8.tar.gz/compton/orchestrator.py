import asyncio
import logging
from functools import partial
from typing import (
    Iterable
)

from .provider import Provider
from .consumer import (
    Consumer,
    ConsumerSentinel
)

from .reducer import Reducer

from .common import (
    match_vector,
    stringify_vector,
    set_hierachical,
    get_hierachical,
    get_partial_hierachical,

    Vector,
    Symbol,
    Payload
)


logger = logging.getLogger(__name__)


class Orchestrator:
    """
    """

    MAX_INIT_RETRIES = 3

    def __init__(
        self,
        reducers: Iterable[Reducer],
        loop=None
    ) -> None:
        self._store = {}
        self._providers = {}
        self._subscribed = {}
        self._reducers = {}

        self._added = set()

        self._apply_reducers(reducers)
        self.__loop = loop

    @property
    def added(self) -> frozenset:
        return frozenset(self._added)

    @property
    def _loop(self) -> asyncio.AbstractEventLoop:
        """Lazy initialize the _loop property
        """

        if self.__loop is not None:
            return self.__loop

        loop = asyncio.get_event_loop()
        self.__loop = loop
        return loop

    def _apply_reducers(
        self,
        reducers: Iterable[Reducer]
    ) -> None:
        saved_reducers = self._reducers

        for reducer in reducers:
            Reducer.check(reducer)

            vector = reducer.vector

            # We set hierachically for reducers, because
            # we allow reducers to do a semi matching
            success, context = set_hierachical(
                saved_reducers, vector, reducer, False)

            if not success:
                raise ValueError(
                    f'a reducer{stringify_vector(context)} already exists'
                )

    def connect(
        self,
        provider: Provider
    ) -> 'Orchestrator':
        """Connect to a provider
        """

        Provider.check(provider)

        vector = provider.vector
        reducer = get_partial_hierachical(self._reducers, vector)

        if reducer is None:
            raise KeyError(
                f'a reducer{stringify_vector(vector)} must be defined before connecting to {provider}'  # noqa:E501
            )

        for provider_vector in self._providers.keys():
            if match_vector(
                provider_vector, vector
            ) or match_vector(
                vector, provider_vector
            ):
                raise KeyError(
                    f'provider{stringify_vector(provider_vector)} exists'
                )

        self._providers[vector] = provider

        dispatch = partial(self.dispatch, vector)
        provider.when_update(dispatch)  # type: ignore

        return self

    def subscribe(
        self,
        consumer: Consumer
    ) -> 'Orchestrator':
        """Let the consumer subscribe to the changes of the store
        """

        Consumer.check(consumer)

        vectors = consumer.vectors
        sentinel = ConsumerSentinel(consumer)

        for vector in vectors:
            if vector not in self._providers:
                vector_str = stringify_vector(vector)
                raise KeyError(f'a provider{vector_str} must be defined before subscribing to {vector_str}')  # noqa:E501

            if vector not in self._subscribed:
                consumers = []
                self._subscribed[vector] = consumers
            else:
                consumers = self._subscribed[vector]

            consumers.append(sentinel)

        return self

    def dispatch(
        self,
        vector: Vector,
        symbol: Symbol,
        payload: Payload
    ) -> None:
        """Dispatch updates to a certain vector.
        This method is mainly used for testing purpose
        """

        self._dispatch(False, vector, symbol, payload)

    def _dispatch(
        self,
        init: bool,
        vector: Vector,
        symbol: Symbol,
        payload: Payload
    ):
        if symbol not in self._added:
            return

        reducer = get_partial_hierachical(self._reducers, vector)

        if reducer is None:
            raise KeyError(
                f'can not process dispatched payload, reason: reducer{stringify_vector(vector)} is not found'  # noqa:E501
            )

        store_vector = (symbol, vector)
        previous = get_hierachical(self._store, store_vector)

        # We need to try-catch this method,
        # because it won't be raised to the outside and interrupt the program.
        # Otherwise it will hard to debug
        try:
            changed, new = reducer.reduce(
                init, vector, symbol, previous, payload
            )
        except Exception as e:
            logger.error('reducer reduce error: %s', e)
            return

        if changed:
            self._set_store(symbol, vector, new)

    def _set_store(
        self,
        symbol,
        vector,
        payload
    ) -> None:
        set_hierachical(self._store, (symbol, vector), payload, True)
        self._emit(symbol, vector)

    def _emit(self, symbol, vector) -> None:
        subscribed = self._subscribed.get(vector, None)

        if not subscribed:
            return

        for consumer_sentinel in subscribed:
            satisfied = consumer_sentinel.satisfy(symbol, vector)

            if not satisfied:
                continue

            consumer_sentinel.process(
                symbol,
                self._get_payloads_by_vectors(
                    symbol,
                    consumer_sentinel.vectors
                ),
                self._loop
            )

    def _get_payloads_by_vectors(self, symbol, vectors):
        store = self._store[symbol]
        return [
            store.get(vector)
            for vector in vectors
        ]

    def add(
        self,
        symbol: Symbol
    ) -> 'Orchestrator':
        """Adds a new stock symbol to the orchestrator
        """

        if symbol not in self._added:
            self._added.add(symbol)

            self._loop.create_task(self._start_providers(symbol))

        return self

    def remove(
        self,
        symbol: Symbol
    ) -> 'Orchestrator':
        """Removes a symbol
        """

        if symbol in self._added:
            self._added.remove(symbol)

            if symbol in self._store:
                del self._store[symbol]

            for provider in self._providers.values():
                provider.remove(symbol)

        return self

    async def _start_providers(self, symbol: Symbol):
        tasks = []

        for provider in self._providers.values():
            task = self._loop.create_task(
                self._start_provider(symbol, provider)
            )

            tasks.append(task)

        await asyncio.wait(tasks)

    async def _start_provider(
        self,
        symbol,
        provider: Provider,
        retries: int = 0
    ):
        try:
            payload = await provider.init(symbol)
        except Exception as e:
            logger.error('init for symbol "%s" failed: %s', symbol, e)

            if retries < self.MAX_INIT_RETRIES:
                return await self._start_provider(
                    symbol,
                    provider,
                    retries + 1
                )

            logger.error('give up init symbol "%s"', symbol)
            return

        self._dispatch(True, provider.vector, symbol, payload)
