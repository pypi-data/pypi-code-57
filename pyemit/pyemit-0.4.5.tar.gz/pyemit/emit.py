import asyncio
import logging
import pickle
import time
from enum import IntEnum
from typing import Callable, Any

logger = logging.getLogger(__name__)


class Engine(IntEnum):
    IN_PROCESS = 0
    REDIS = 1


# for aio-redis mq only
_pub_conn = None
_sub_conn = None

# msg => {"queue": aioredis.Channel, "handlers": handlers}
_registry = {}
_heart_beat = 0
_started = False
_engine = Engine.IN_PROCESS
__rpc_calls__ = {}
_rpc_client_channel = '__emit_rpc_client_channel__'
_rpc_server_channel = '__emit_rpc_server_channel__'
_dsn = None
_start_server = False


def on(event, exchange=""):
    """
    提供了消息注册的装饰器实现
    Args:
        event:
        exchange:
    Returns:

    """

    def decorator(func):
        register(event, func, exchange)

    return decorator


def register(event: str, handler: Callable, exchange=""):
    """
    :param event:
    :param handler:
    :param exchange:
    :return:
    """
    global _registry

    event = f"{exchange}/{event}"
    item = _registry.get(event, {"handlers": set()})
    item['handlers'].add(handler)
    _registry[event] = item

    if _started:
        # in this case, we need manually bind msg, handler with a queue/channel
        asyncio.create_task(_bind(event))


async def _bind(event: str):
    global _registry, _engine, _sub_conn, _pub_conn

    item = _registry.get(event)
    if _engine == Engine.IN_PROCESS:
        if item.get('queue') is None:
            queue = asyncio.Queue()
            await queue.join()
            item['queue'] = queue
        else:
            logger.debug("msg %s is already bound to local queue, skipped", event)
    else:
        if item.get('queue') is None:
            response = await _sub_conn.subscribe(event)
            if response:
                item['queue'] = response[0]
            else:
                logger.warning("failed to bind msg %s to remote queue", event)
        else:
            logger.debug("msg %s is already bound to remote queue, skipped", event)

    asyncio.create_task(_listen(event))


async def _listen(event: str):
    global _registry, _engine

    async def get_and_invoke(name, message: dict):
        # handlers may add later, so we put call in the loop
        handlers = _registry.get(name, {}).get("handlers", [])
        if not handlers:
            logger.debug("discarded msg due to no handlers attached: %s", message)
            return

        for func in handlers:
            func_name = getattr(func, "__name__", None)
            logger.debug("%s is handling message: %s", func_name or func, message)
            await func(message)

    queue = _registry.get(event, {}).get('queue')
    if queue is None:
        logger.warning("failed to found queue to listen for msg %s", event)
        return

    logger.info("listening on %s", queue)
    if _engine == Engine.IN_PROCESS:
        while True:
            msg = await queue.get()
            try:
                msg = pickle.loads(msg)
                logger.debug('emit received msg: %s', msg)
                await get_and_invoke(event, msg)
            except Exception as e:
                logger.warning("msg %s caused exception", msg)
                logger.exception(e)
            finally:
                queue.task_done()
    else:
        import aioredis
        try:
            while await queue.wait_message():
                msg = await queue.get()

                try:
                    msg = pickle.loads(msg)
                    logger.debug('emit received msg: %s', msg)
                    await get_and_invoke(event, msg)
                except Exception as e:
                    logger.warning("msg %s caused exception", msg)
                    logger.exception(e)
        except aioredis.errors.ConnectionClosedError:
            logger.warning('connection with Redis server closed, retry connect')
            await stop()
            await start(Engine.REDIS, heart_beat=_heart_beat, dsn=_dsn, start_server=_start_server)


async def _client_handle_rpc_call(msg: dict):
    sn = msg.get("_sn_")
    if sn is None:
        logger.warning("rpc call msg must contains _sn_ key: %s", msg)
        return

    waited = __rpc_calls__.get(sn)
    if waited is not None:
        msg.pop('_sn_')
        waited['result'] = msg
        waited['event'].set()
    else:
        logger.debug("emit received unsolicited message: %s", sn)


async def start(engine: Engine = Engine.IN_PROCESS, start_server=False, heart_beat=0, **kwargs):
    """

    Args:
        engine:
        start_server:
        heart_beat:
    """
    global _started, _pub_conn, _sub_conn, _registry, _heart_beat, _engine, _rpc_client_channel, _dsn, \
        _start_server
    if _started:
        logger.info("emit is already started.")
        return

    logger.info("starting pyemit with registry: %s", _registry)

    _engine = engine
    _heart_beat = heart_beat
    _start_server = start_server
    _dsn = kwargs.get("dsn", None)

    if _engine == Engine.REDIS:
        if _dsn is None:
            raise SyntaxError("When engine is REDIS, param 'dsn' is required.")

        import aioredis

        register(_rpc_client_channel, _client_handle_rpc_call)
        if _start_server:
            register(_rpc_server_channel, _server_rpc_handler)

        _pub_conn = await aioredis.create_redis(_dsn)
        _sub_conn = await aioredis.create_redis(_dsn)

        if _heart_beat > 0:
            register('heartbeat', _on_heart_beat)
    else:
        register(_rpc_client_channel, _client_handle_rpc_call)
        register(_rpc_server_channel, _server_rpc_handler)

    # bind registered channels
    for channel in _registry.keys():
        await _bind(channel)

    if _heart_beat > 0 and engine == Engine.REDIS:
        await emit("heartbeat", {"msg": 'heartbeat', "time": time.time()})

    _started = True


async def emit(channel: str, message: Any = None, exchange=""):
    """
    publish a message to channel.
    :param channel: the name of channel
    :param message:
    :return:
    """
    global _registry, _engine, _pub_conn

    channel = f"{exchange}/{channel}"
    logger.debug('send message on channel %s: %s', channel, message)
    if not isinstance(message, bytes):
        message = pickle.dumps(message, protocol=4)

    if _engine == Engine.IN_PROCESS:
        queue = _registry.get(channel, {}).get("queue", None)
        if queue is None:
            logger.warning(f"channel {channel} has no listener registered, skipped.")
            return
        queue.put_nowait(message)
    elif _engine == Engine.REDIS:
        import aioredis
        try:
            await _pub_conn.publish(f"{channel}", message)
        except aioredis.errors.ConnectionClosedError:
            logger.warning('connection with Redis server closed, retry connect')
            await stop()
            await start(Engine.REDIS, heart_beat=_heart_beat, dsn=_dsn, start_server=_start_server)
            raise ConnectionError


async def rpc_send(remote) -> Any:
    """
    emit msg and wait response back. The func will add __emit_sn__ to the dict, and the server should echo the serial
    number
    back.
    Args:
        remote:

    Returns:

    """
    global __rpc_calls__
    sn = remote.sn

    event = asyncio.Event()

    __rpc_calls__[sn] = {
        "event":  event,
        "result": None
    }

    logger.debug("sending rpc msg to server: %s", sn)
    await emit(_rpc_server_channel, pickle.dumps(remote, protocol=4))
    try:
        await asyncio.wait_for(event.wait(), remote.timeout)
    except asyncio.TimeoutError:
        raise TimeoutError

    response = __rpc_calls__.get(sn, {}).get("result")
    return pickle.loads(response.get('_data_'))


async def rpc_respond(msg: dict):
    global __rpc_calls__
    logger.debug("responding rpc msg to client: %s", msg['_sn_'])
    await emit(_rpc_client_channel, msg)


async def _server_rpc_handler(remote):
    await remote.server_impl()


def unsubscribe(channel: str, handler: Callable, exchange=""):
    """
    stop subscribe message from channel
    :param channel:
    :param handler:
    :return:
    """
    global _registry, _engine

    channel = f"{exchange}/{channel}"
    if channel not in _registry.keys():
        logger.warning("%s is not registered", channel)
        return

    handlers: set = _registry.get(channel, {}).get("handlers", set())
    try:
        handlers.remove(handler)
    except KeyError:
        logger.warning("%s is not registered as handler of %s", handler.__name__, channel)

    _registry[channel]["handlers"] = handlers


async def _on_heart_beat(msg):
    """
    :param msg:
    :return:
    """
    logger.debug("mq received heart beat: %s", msg)
    await asyncio.sleep(_heart_beat)
    await emit("heartbeat", {"msg": 'heartbeat', "time": time.time()})


async def stop():
    global _started, _engine, _registry
    logger.info("stopping emit...")
    _started = False

    if _engine == Engine.REDIS:
        _sub_conn.close()
        await _sub_conn.wait_closed()

    for binding in _registry.values():
        binding['queue'] = None

    logger.info("emit stopped.")
