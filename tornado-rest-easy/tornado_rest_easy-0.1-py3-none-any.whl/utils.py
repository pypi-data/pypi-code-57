import json
from datetime import datetime

import tornado


def run_in_executor(executor, func, *args, **kwargs):
    """Run a blocking function in a separate thread in the tornado ioloop.

    Copied from function which is added in a later version: https://www.tornadoweb.org/en/stable/_modules/tornado/ioloop.html#IOLoop.run_in_executor

    Improves a little on the function by allowing kwargs to be passed too instead of the
    suggestion of using partial.
    """
    c_future = executor.submit(func, *args, **kwargs)
    t_future = tornado.concurrent.Future()
    loop = tornado.ioloop.IOLoop.current()
    loop.add_future(c_future, lambda f: tornado.concurrent.chain_future(f, t_future))
    return t_future


def api_serialize(data=None, error=None, msg=None, **kwargs):
    d = {'data': data,
         'ts': datetime.now().isoformat(),
         'error': error,
         'msg': msg,
         **kwargs}
    return json.dumps(d)