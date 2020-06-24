from collections import namedtuple
from asyncio import create_task, sleep
from time import time
from uuid import uuid4
import inspect

from msgpack import packb, unpackb

Dispatcher = namedtuple("Dispatcher", ["listen", "unlisten", "handler", "callback_handler", "resolve"])

async def extract_co(co_or_v):
    if inspect.iscoroutine(co_or_v):
        return await co_or_v

    return co_or_v

def make_dispatcher(queue, get_redis, max_ttl = 60, on_exception = None):
    redis         = None
    listener_task = None
    handlers      = {}
    stopped       = False

    processing_map = f"{queue}:processing"
    pending_map    = f"{queue}:pending"

    async def get_redis_():
        nonlocal redis

        if redis is None:
            redis = await get_redis()

        return redis

    async def handle_exception(e):
        if on_exception is not None:
            return await extract_co(on_exception(e))

    def expand_task(task):
        keys = ["eta", "id", "kind", "args", "kwargs", "value", "has_callback"]

        return " ".join(f"{k}={task[k]}" for k in keys if k in task)

    def repr_task(label, task, label_length=16):
        now = int(time())
        return f"{label.ljust(label_length)}: now={now} {expand_task(task)}"

    # redis actions >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    async def enqueue(task):
        r = await get_redis_()

        await r.zadd(queue, task["eta"], packb(task))

    async def dequeue():
        r = await get_redis_()

        taskb = await r.eval("""
            local queue          = KEYS[1]
            local processing_map = KEYS[2]
            local now            = tonumber(ARGV[1])

            local ret = redis.call("zpopmin", queue)

            if #ret == 0 then
                return nil
            end

            local taskb     = ret[1]
            local task      = cmsgpack.unpack(taskb)
            local task_id   = task.id
            local wip_taskb = cmsgpack.pack({ idle_from = now, task = task })

            redis.call("hset", processing_map, task_id, wip_taskb)

            return taskb
        """, [queue, processing_map], [int(time())])

        task = taskb and unpackb(taskb)

        return task

    async def re_enqueue(task_id):
        r = await get_redis_()

        await r.eval("""
            local queue          = KEYS[1]
            local processing_map = KEYS[2]
            local task_id        = ARGV[1]

            local wip_taskb = redis.call("hget", processing_map, task_id)

            if not wip_taskb then
                return
            end

            local wip_task  = cmsgpack.unpack(wip_taskb)
            local task      = wip_task.task
            local taskb     = cmsgpack.pack(task)

            redis.call("hdel", processing_map, task_id)
            redis.call("zadd", queue, task.eta, taskb)
        """, [queue, processing_map], [task_id])

    async def wait_for_resolve(task):
        r = await get_redis_()

        await r.hset(pending_map, task["id"], packb(task))

    async def resolve(task_id, value = None):
        r = await get_redis_()

        await r.eval("""
            local queue       = KEYS[1]
            local pending_map = KEYS[2]
            local task_id     = ARGV[1]
            local now         = tonumber(ARGV[2])
            local value       = cmsgpack.unpack(ARGV[3])

            local pending_taskb = redis.call("hget", pending_map, task_id)

            if not pending_taskb then
                return
            end

            local pending_task = cmsgpack.unpack(pending_taskb)

            pending_task.value = value
            pending_task.eta   = now

            pending_taskb = cmsgpack.pack(pending_task)

            redis.call("hdel", pending_map, task_id)
            redis.call("zadd", queue, now, pending_taskb)
        """, [queue, pending_map], [task_id, int(time()), packb(value)])

    async def ack(task_id):
        r = await get_redis_()

        await r.hdel(processing_map, task_id)

    # decorators >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def handler(kind = None):
        def wrapper(f):
            kind_ = kind or f"{f.__module__}.{f.__qualname__}"

            handlers[kind_] = f

            async def execute_at(eta = None, args = [], kwargs = {}):
                id_ = str(uuid4())

                if eta is None:
                    eta = int(time())

                task = {
                    "eta"          : eta,
                    "kind"         : kind_,
                    "id"           : id_,
                    "args"         : args,
                    # here I use the kv pairs instead of a map to workaround an issue that
                    # empty table will be converted to msgpack array inside lua
                    "kwargs"       : list(kwargs.items()),
                    "has_callback" : False,
                }

                await enqueue(task)

                return task

            def delay_by(secs, args = [], kwargs = {}):
                eta = int(time()) + secs

                return execute_at(eta=eta, args=args, kwargs=kwargs)

            def g(*args, **kwargs):
                return execute_at(args=args, kwargs=kwargs)

            g.execute_at = execute_at
            g.delay_by   = delay_by

            return g

        return wrapper

    def callback_handler(remote_call, kind = None):
        def wrapper(f):
            kind_ = kind or f"{f.__module__}.{f.__qualname__}"

            handlers[kind_] = f

            async def g(*args, **kwargs):
                id_ = str(uuid4())

                task = {
                    "eta"          : None,
                    "kind"         : kind_,
                    "id"           : id_,
                    "args"         : args,
                    "kwargs"       : list(kwargs.items()),
                    "has_callback" : True,
                }

                # the two calls below is not strictly safe, cuz there is a situation
                # that remote callback executed earlier than the second call
                await remote_call(task)
                await wait_for_resolve(task)

            return g

        return wrapper

    async def handle(task):
        try:
            handler = handlers.get(task["kind"])

            if handler is not None:
                args   = task["args"]
                kwargs = dict(task["kwargs"])

                handler_ret = handler(*args, **kwargs)

                if inspect.iscoroutine(handler_ret):
                    handler_ret = await handler_ret

                if task["has_callback"]:
                    callback_ret = handler_ret(task.get("value", None))

                    if inspect.iscoroutine(callback_ret):
                        await callback_ret

                await ack(task["id"])

                print(repr_task("acknowledged", task))
        except Exception as e:
            await handle_exception(e)

    async def check_process():
        try:
            r = await get_redis_()

            wip_tasks = await r.hgetall(processing_map)
            now = int(time())

            for id_, taskb in wip_tasks.items():
                wip_task  = unpackb(taskb)
                idle_from = wip_task["idle_from"]
                task      = wip_task["task"]

                if now - idle_from > max_ttl:
                    await re_enqueue(id_)
        except Exception as e:
            await handle_exception(e)

    async def main():
        counter = 0
        while True:
            try:
                if not stopped:
                    task = await dequeue()

                    if task is not None:
                        if task["eta"] <= int(time()):
                            print(repr_task("handling", task))

                            create_task(handle(task))
                            continue
                        else:
                            await re_enqueue(task["id"])

                await sleep(1)

                if counter == 0:
                    create_task(check_process())

                counter = (counter + 1) % 60
            except Exception as e:
                await handle_exception(e)

    def listen():
        nonlocal listener_task

        assert listener_task is None, "already listening"

        listener_task = create_task(main())

    async def unlisten():
        nonlocal listener_task, stopped

        assert listener_task is not None, "not listening"

        stopped = True

        r = await get_redis_()
        while True:
            total_processing = await r.hlen(processing_map)

            print("processing:", total_processing)
            if total_processing == 0:
                break

            await sleep(1)

        listener_task.cancel()
        listener_task = None

    dispatcher = Dispatcher(
        handler          = handler,
        callback_handler = callback_handler,
        resolve          = resolve,
        listen           = listen,
        unlisten         = unlisten,
    )

    return dispatcher
