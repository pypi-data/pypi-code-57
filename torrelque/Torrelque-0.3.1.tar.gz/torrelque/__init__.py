'''Asynchronous Redis-backed reliable queue package.'''


import json
import uuid
import time
import enum
import asyncio
import hashlib
import logging
import contextlib

import aredis


__all__ = 'Torrelque', 'TorrelqueTaskStatus'

logger = logging.getLogger(__package__)


class TorrelqueTaskStatus(enum.IntEnum):
    '''Task status.'''

    PENDING = 0
    '''Task is enqueued.'''

    WORKING = 1
    '''Task is dequeued.'''

    DELAYED = 2
    '''Task is delayed.'''

    COMPLETED = 3
    '''Task is released, as the result of successful completion.'''

    REJECTED = 4
    '''Task is released, as the result of (multiple) failed attempts.'''

    def isfinal(self):
        '''Tells whether the status is final.'''

        return self in (self.COMPLETED, self.REJECTED)


class Torrelque:
    '''
    Reliable work queue.

    :param redis: Redis client instance.
    :param queue:
        Name of the queue. Must match across producers and consumers.
    :param serialiser:
        An object with ``dumps`` and ``loads`` that (de)serialises
        task bodies.
    '''

    task_timeout = 300
    '''
    Default timeout for a task in the "working" set to be
    considered stale.
    '''

    sweep_interval = 30
    '''Default interval between sweep calls, when sweep is scheduled.'''

    result_ttl = 3600
    '''Default time-to-live of a task result (when applicable).'''

    keys = {
        'pending' : 'pending',  # list
        'working' : 'working',  # sorted set
        'delayed' : 'delayed',  # sorted set
        'tasks'   : 'tasks',    # hash
        'task'    : 'task'      # prefix for hashes
    }
    '''
    Queue Redis key name mapping.

    On initialisation the values are prefixed with the queue name, and
    the new dictionary is rebound to the instance.
    '''

    _serialiser = None
    '''
    Task data serialiser that converts task object into and from string
    representation.
    '''

    _redis = None
    '''Redis client.'''

    _sweep_task = None
    '''Periodic sweep asyncio task.'''

    _keyspace_notification_enabled = False
    '''
    Flag indicates that Redis keyspace notification were found
    correctly configured, and further tests should be omitted.
    '''

    def __init__(self, redis: aredis.StrictRedis, *, queue='trq', serialiser=json):
        if not isinstance(redis, aredis.StrictRedis):
            raise ValueError('aredis.StrictRedis instance expected')

        self._redis = redis
        self._serialiser = serialiser

        self.keys = {k: f'{queue}:{v}' for k, v in self.keys.items()}

    def _get_state_key(self, task_id):
        return '{}:{}'.format(self.keys['task'], task_id)

    async def _call_script(self, script, keys, args):
        digest = hashlib.sha1(script.encode()).hexdigest()
        try:
            result = await self._redis.evalsha(digest, len(keys), *(keys + args))
        except aredis.NoScriptError:
            result = await self._redis.eval(script, len(keys), *(keys + args))

        return result

    async def _enqueue(self, pipe, task, task_timeout, delay):
        task_timeout = task_timeout or self.task_timeout
        task_id = uuid.uuid1().hex
        task_data = self._serialiser.dumps(task)
        task_state_key = self._get_state_key(task_id)

        if delay:
            await pipe.zadd(self.keys['delayed'], time.time() + delay, task_id)
            await pipe.hset(task_state_key, 'status', TorrelqueTaskStatus.DELAYED.value)
        else:
            await pipe.lpush(self.keys['pending'], task_id)
            await pipe.hset(task_state_key, 'status', TorrelqueTaskStatus.PENDING.value)

        await pipe.hset(self.keys['tasks'], task_id, task_data)
        await pipe.hset(task_state_key, 'enqueue_time', time.time())
        await pipe.hset(task_state_key, 'timeout', task_timeout)

        return task_id

    async def enqueue(
        self,
        task,
        *,
        task_timeout: float = None,
        delay: float = None,
        pipeline: 'aredis.pipeline.StrictPipeline' = None
    ) -> str:
        '''
        Put a task on the queue optionally providing its timeout and delay.

        :param task: Arbitrary serialisable task payload.
        :param task_timeout:
            Time since the task's processing start after which it is
            considered stale.
        :param delay:
            Number of seconds to delay processing of the task, i.e.
            putting it into the "pending" list. Note that the sweep
            must be scheduled for the delayed tasks to return, and
            the delay only has effect after the sweep execution.
        :param pipeline:
            External Redis pipline that allows for bulk enqueue.
        :return: Task identifier.
        '''

        if pipeline is not None:
            task_id = await self._enqueue(pipeline, task, task_timeout, delay)
        else:
            async with await self._redis.pipeline(transaction=True) as pipeline:
                task_id = await self._enqueue(pipeline, task, task_timeout, delay)
                await pipeline.execute()

        return task_id

    async def _dequeue(self, timeout):
        # This trick with BRPOPLPUSH makes it possible to make dequeue()
        # blocking, thus avoid overhead and latency caused by polling.
        # Later on the ``task_id`` LREM will be applied, which is less
        # efficient that LPOP or RPOP, but because the rotation has just
        # occurred the entry being deleted is at the beginning of the
        # list and LREM complexity is close to O(1).
        task_id = await self._redis.brpoplpush(
            self.keys['pending'], self.keys['pending'], timeout=timeout or 0
        )
        if not task_id:
            raise TimeoutError

        script = r'''
            local pending, working, tasks = unpack(KEYS)
            local task_id = ARGV[1]
            local now = ARGV[2]
            local working_status = ARGV[3]

            local removed = redis.call('LREM', pending, 1, task_id)
            if removed == 0 then
                return {0, 'null'}
            end

            local task_data = redis.call('HGET', tasks, task_id)

            local state_key = KEYS[4] .. ':' .. task_id
            local task_timeout = redis.call('HGET', state_key, 'timeout')
            local stale = now + task_timeout
            redis.call('ZADD', working, stale, task_id)

            redis.call('HSET', state_key, 'last_dequeue_time', now)
            redis.call('HSET', state_key, 'status', working_status)
            redis.call('HINCRBY', state_key, 'dequeue_count', 1)

            return {task_id, task_data}
        '''

        keys = [self.keys[k] for k in ('pending', 'working', 'tasks', 'task')]
        args = [task_id, time.time(), TorrelqueTaskStatus.WORKING.value]
        task_id, task_data = await self._call_script(script, keys, args)

        if task_id:
            return task_id.decode(), self._serialiser.loads(task_data)
        else:
            return None, None

    async def dequeue(self, timeout: int = None) -> tuple:
        '''
        Get a task from the queue with optional timeout.

        :param timout:
            Time to wait until the task is available.
            Note that Redis only supports an integer timeout.
        :raises TimeoutError:
            If timeout was provided and there was no result within it.
        :return: Tuple of task identifier and deserialised task payload.
        '''

        start = time.monotonic()
        iter_timeout = timeout
        while True:
            task_id, task_data = await self._dequeue(iter_timeout)
            # task_id is None when another consumer "won" the task
            if task_id:
                return task_id, task_data
            elif timeout:
                elapsed = time.monotonic() - start
                if elapsed > timeout:
                    raise TimeoutError('Total dequeue attempts timed out')
                else:
                    iter_timeout = max(1, round(timeout - elapsed))

    async def requeue(self, task_id: str, delay: float = None, *, task_timeout: float = None):
        '''
        Return failed task into the queue with optional delay.

        :param task_id: Task identifier.
        :param delay:
            Number of seconds to delay returning the task back into
            the "pending" list. Note that the sweep must be scheduled
            for the delayed tasks to return, and the delay only has
            effect after the sweep execution.
        :param task_timeout:
            Redefine task timeout, which is the time since the task's
            processing start after which it is considered stale.
        '''

        expected = []
        async with await self._redis.pipeline(transaction=True) as pipe:
            await pipe.zrem(self.keys['working'], task_id)
            expected.append(1)

            task_state_key = self._get_state_key(task_id)
            if not delay:
                await pipe.lpush(self.keys['pending'], task_id)
                await pipe.hset(task_state_key, 'last_requeue_time', time.time())
                await pipe.hincrby(task_state_key, 'requeue_count', 1)
                await pipe.hset(task_state_key, 'status', TorrelqueTaskStatus.PENDING.value)
                expected.extend([..., ..., ..., 0])
            else:
                await pipe.zadd(self.keys['delayed'], time.time() + delay, task_id)
                await pipe.hset(task_state_key, 'status', TorrelqueTaskStatus.DELAYED.value)
                expected.extend([1, 0])

            if task_timeout:
                await pipe.hset(task_state_key, 'timeout', task_timeout)
                expected.append(0)

            result = await pipe.execute()

        if not all(expc == actl or expc is ... for expc, actl in zip(expected, result)):
            logger.warning('Inconsistent requeue of task:%s: %s', task_id, result)

    async def release(
        self,
        task_id: str,
        *,
        result=None,
        result_ttl: int = None,
        status: TorrelqueTaskStatus = TorrelqueTaskStatus.COMPLETED
    ):
        '''
        Remove finished task from the queue.

        Unless ``result`` is specified, all task information is removed
        from the queue immediately.

        Since there's no dead letter queue, tasks that have exceeded
        allowed number of retries should also be released, possibly
        with ``TorrelqueTaskStatus.REJECTED`` status if producer is
        interested in the status.

        :param task_id: Task identifier.
        :param result:
            Arbitrary serialisable task result. If ``result`` is
            ``None`` task state key is removed immediately on release.
        :param result_ttl:
            Number of seconds to keep task state key after release.
            Override of default result TTL.
        :param status:
            Task status to set on release. It only apples when result
            is not ``None``.
        '''

        if status is not None and not status.isfinal():
            raise ValueError(f'Invalid status for released task: {status}')

        expected = []
        async with await self._redis.pipeline(transaction=True) as pipe:
            await pipe.zrem(self.keys['working'], task_id)
            await pipe.hdel(self.keys['tasks'], task_id)
            expected.extend([1, 1])

            task_state_key = self._get_state_key(task_id)
            if result is not None:
                await pipe.hset(task_state_key, 'result', self._serialiser.dumps(result))
                await pipe.hset(task_state_key, 'release_time', time.time())
                await pipe.hset(task_state_key, 'status', status.value)
                expected.extend([1, 1, 0])

                result_ttl = result_ttl if result_ttl is not None else self.result_ttl
                await pipe.expire(task_state_key, result_ttl)
                expected.append(1)
            else:
                await pipe.delete(task_state_key)
                expected.append(1)

            result = await pipe.execute()

        if expected != result:
            logger.warning('Inconsistent release of task:%s: %s', task_id, result)

    async def _check_keyspace_notification_config(self):
        if not self._keyspace_notification_enabled:
            config = await self._redis.config_get('notify-keyspace-events')
            notify_config = set(config['notify-keyspace-events'])
            # See https://redis.io/topics/notifications#configuration
            if {'K', 'A'} - notify_config and {'K', 'g', 'h'} - notify_config:
                raise RuntimeError('Redis notify-keyspace-events must include KA or Kgh')
            self._keyspace_notification_enabled = True

    async def _get_keyspace_notification_message(self, pubsub, timeout):
        listen_task = asyncio.get_event_loop().create_task(pubsub.listen())
        try:
            message = await asyncio.wait_for(listen_task, timeout)
            # This is the effect of ignore_subscribe_messages
            if message is None:
                message = await self._get_keyspace_notification_message(pubsub, timeout)
        except asyncio.TimeoutError as ex:
            # On cancellation pubsub.parse_response returns None, which
            # pubsub.handle_message cannot hanle.
            with contextlib.suppress(TypeError):
                await listen_task
            raise TimeoutError from ex
        else:
            return message

    async def watch(self, task_id: str, *, timeout: float = None):
        '''
        Watch task status change until it's released from the queue.

        .. note::

           This method relies on ``notify-keyspace-events`` introduced
           in Redis 2.8. The configuration must have generic and hash
           commands enabled. That is, the configuration must include
           either ``KA`` or ``Kgh``.

        :param task_id: Task identifier.
        :param timeout: Timeout for watching.
        :raises RuntimeError:
            If ``notify-keyspace-events`` is not configured properly.
        :raises TimeoutError:
            If ``watch`` has taken longer than ``timeout``.
        :raises LookupError: If the task state key is not found.
        :return:
            Asynchronous generator that yields task state dictionaries
            as returned by :py:meth:`.get_task_state`. Generator stops
            when the task is released. If the task is released without
            result, generator won't yield ``dict`` with final status.
        '''

        start = time.monotonic()

        await self._check_keyspace_notification_config()

        task_state = await self.get_task_state(task_id)
        yield task_state

        status = task_state['status']
        if status.isfinal():
            return

        with contextlib.closing(self._redis.pubsub(ignore_subscribe_messages=True)) as pubsub:
            dbn = self._redis.connection_pool.connection_kwargs['db']
            await pubsub.subscribe('__keyspace@{}__:{}'.format(dbn, self._get_state_key(task_id)))

            iter_timeout = timeout
            while True:
                message = await self._get_keyspace_notification_message(pubsub, iter_timeout)
                if message['data'] == b'del':
                    return  # Released without result
                elif message['data'] == b'hset':
                    try:
                        task_state = await self.get_task_state(task_id)
                    except LookupError:
                        return  # Race condition with release

                    if task_state['status'] != status:
                        status = task_state['status']
                        yield task_state
                        if status.isfinal():
                            return

                if timeout is not None:
                    iter_timeout = timeout - (time.monotonic() - start)

    async def sweep(self) -> int:
        '''
        Execute the task sweep.

        Return stale tasks from "working" set into "pending" list.
        Move due delayed tasks from "delayed" set into "pending" list.

        :return: Number of tasks requeued.
        '''

        script = '''
            local function requeue(pending_key, target_key, state_prefix, now, pending_status)
                local task_ids = redis.call('ZRANGEBYSCORE', target_key, 0, now)
                if #task_ids == 0 then
                    return 0
                end

                redis.call('LPUSH', pending_key, unpack(task_ids))
                redis.call('ZREM', target_key, unpack(task_ids))

                local state_key
                for _, task_id in ipairs(task_ids) do
                    state_key = state_prefix .. ':' .. task_id
                    redis.call('HSET', state_key, 'last_requeue_time', now)
                    redis.call('HSET', state_key, 'status', pending_status)
                    redis.call('HINCRBY', state_key, 'requeue_count', 1)
                end

                return #task_ids
            end

            local pending, working, delayed, state = unpack(KEYS)
            local now = ARGV[1]
            local pending_status = ARGV[2]

            return
                requeue(pending, working, state, now, pending_status) +
                requeue(pending, delayed, state, now, pending_status)
        '''

        keys = [self.keys[k] for k in ('pending', 'working', 'delayed', 'task')]
        args = [time.time(), TorrelqueTaskStatus.PENDING.value]
        result = await self._call_script(script, keys, args)

        return result

    async def _sweep_runner(self):
        while True:
            start = time.monotonic()
            try:
                sweeped = await self.sweep()
            except aredis.RedisError:
                logger.exception('Sweep has failed with Redis error, continuing')
            except Exception:
                logger.exception('Sweep has failed with unexpected error, stopping')
                break
            else:
                logger.debug('Sweep has requeued %d tasks', sweeped)

            await asyncio.sleep(self.sweep_interval - (time.monotonic() - start))

    def schedule_sweep(self, interval: float = None):
        '''
        Schedule the sweep in a background coroutine.

        :param interval: Override of default sweep interval.
        '''

        if interval:
            self.sweep_interval = interval

        self._sweep_task = asyncio.get_event_loop().create_task(self._sweep_runner())

    def unschedule_sweep(self):
        '''Unschedule the sweep in a background coroutine.'''

        assert self._sweep_task
        # CancelledError is not caught in the _sweep_runner is there's nothing to await
        self._sweep_task.cancel()

    async def get_queue_stats(self) -> dict:
        '''
        Get queue counters.

        :return: Dictionary containing queue counters.

        ::

            {
                'tasks'   : 2,
                'pending' : 1,
                'working' : 1,
                'delayed' : 0,
            }

        '''

        async with await self._redis.pipeline(transaction=True) as pipe:
            await pipe.hlen(self.keys['tasks'])
            await pipe.llen(self.keys['pending'])
            await pipe.zcard(self.keys['working'])
            await pipe.zcard(self.keys['delayed'])
            result = await pipe.execute()

        return dict(zip(('tasks', 'pending', 'working', 'delayed'), result))

    async def get_task_state(self, task_id: str) -> dict:
        '''
        Get task state.

        :param task_id: Task identifier.
        :raises LookupError: If the task state key is not found.
        :return: Dictionary containing task counters and timestamps.

        ::

            {
                'status'             : TorrelqueTaskStatus.WORKING,
                'timeout'            : 120.0,
                'enqueue_time'       : 1234567890.0,
                'last_dequeue_time'  : 1234567892.0,  # can be None
                'dequeue_count'      : 2,
                'last_requeue_time'  : 1234567891.0,  # can be None
                'requeue_count'      : 1,
                'result'             : 42,
                'release_time'       : 4294967295.0,
            }

        :raises LookupError: If no task state key found.
        '''

        result = await self._redis.hgetall(self._get_state_key(task_id))
        if not result:
            raise LookupError

        return {
            'status'             : TorrelqueTaskStatus(int(result[b'status'])),
            'timeout'            : float(result[b'timeout']),
            'enqueue_time'       : float(result[b'enqueue_time']),
            'last_dequeue_time'  : float(result.get(b'last_dequeue_time', 0)) or None,
            'dequeue_count'      : int(result.get(b'dequeue_count', 0)),
            'last_requeue_time'  : float(result.get(b'last_requeue_time', 0)) or None,
            'requeue_count'      : int(result.get(b'requeue_count', 0)),
            'release_time'       : float(result.get(b'release_time', 0)) or None,
            'result'             : (
                self._serialiser.loads(result[b'result'])
                if result.get(b'result') is not None else None
            )
        }
