import tornado
import tornado.web

from .path import RestFunction
from .tree import PathDispatcher
from .utils import api_serialize, run_in_executor


def get(uri, response_type='json'):
    def wrapped(f):
        return RestFunction(f, uri, 'GET', response_type=response_type)
    return wrapped


def post(uri, response_type='json'):
    def wrapped(f):
        return RestFunction(f, uri, 'POST', response_type=response_type)
    return wrapped


def delete(uri, response_type='json'):
    def wrapped(f):
        return RestFunction(f, uri, 'DELETE', response_type=response_type)
    return wrapped


def head(uri, response_type='json'):
    def wrapped(f):
        return RestFunction(f, uri, 'HEAD', response_type=response_type)
    return wrapped


def put(uri, response_type='json'):
    def wrapped(f):
        return RestFunction(f, uri, 'PUT', response_type=response_type)
    return wrapped


def patch(uri, response_type='json'):
    def wrapped(f):
        return RestFunction(f, uri, 'PATCH', response_type=response_type)
    return wrapped


class RestfulMetaType(type):
    """
    Registers rest class methods with the class's dispatcher.
    """
    def __new__(typ, classname, mro, d):
        x = super().__new__(typ, classname, mro, d)
        x.endpoint_dispatcher = PathDispatcher()
        x.response_meta = dict()
        for name, method in d.items():
            if isinstance(method, RestFunction):
                x.endpoint_dispatcher.register_rest_function(method)
        return x

    def get_paths(cls):
        return cls.endpoint_dispatcher.regex_paths

    def get_handlers(cls, initialize_kwargs=dict()):
        return [(p, cls, initialize_kwargs) for p in cls.get_paths()]


class RestfulHandler(tornado.web.RequestHandler):
    """RestfulHandler

    Restful wrapper to the tornado RequestHandler. Allows you to simultaneously overload
    the get/post methods of the class and specify the url. This lets you map a url to a
    specific function. It also lets you specify arguments in the url via an easy to read
    format rather than regex. This format includes argument parsing.

    The method overloading is done via the `PathDispatcher` class. When an http request
    comes in, the request path is used to lookup the associated function. By overriding
    the metaclass, new subclasses get their rest methods registered with the dispatcher.

    Example
    -------
    class WidgetHandler(RestfulHandler, metaclass=RestfulMetaType):

        @get('/widgets')
        def all_widgets(self):
            return [widget1, widget2, ...]

        @get('/widgets/<int:id>')
        def get_widget(self, id):
            return widgets[id]

        @post('/widgets'):
        def add_widget(self):
            return 'Widget added'

    app = Application(WidgetHandler.get_handlers(dict(db=db))
    """
    api_serialize = api_serialize
    executor = None

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, PATCH, DELETE, OPTIONS')
        self.set_header('Access-Control-Allow-Headers', 'contentType, x-requested-with, Content-Type')

    def write_error(self, status_code, **kwargs):
        msg = 'Unknown Error'
        if 'exc_info' in kwargs:
            msg = str(kwargs['exc_info'][1])
        elif 'reason' in kwargs:
            msg = kwargs['reason']
        self.set_header('Content-Type', 'application/json')
        self.write(type(self).api_serialize(error=msg))

    async def options(self, *args, **kwargs):
        self.set_status(204)
        self.finish()

    async def get(self, *args, **kwargs):
        await self._exe('GET')

    async def post(self, *args, **kwargs):
        await self._exe('POST')

    async def delete(self, *args, **kwargs):
        await self._exe('DELETE')

    async def head(self, *args, **kwargs):
        await self._exe('HEAD')

    async def patch(self, *args, **kwargs):
        await self._exe('PATCH')

    async def put(self, *args, **kwargs):
        await self._exe('PUT')

    async def _exe(self, method):
        op = self.endpoint_dispatcher.dispatch(self.request.path, method)
        if self.executor is None:
            res = op(self, *self.path_args)
        else:
            res = await run_in_executor(self.executor, op, self, *self.path_args)

        #prevent writing two responses
        if self._finished:
            return

        msg = ""
        if isinstance(res, tuple) and len(res) == 2:
            res, msg = res
        # response_type can be set in the function by annotation but we may not want it explicitly set
        if self.response_meta and "response_type" in self.response_meta:
            response_type = self.response_meta['response_type']
        else:
            response_type = op.response_type
        if response_type == 'json':
            self.set_header('Content-Type', 'application/json')
            self.write(type(self).api_serialize(data=res, msg=msg, **type(self).response_meta))
        elif response_type == 'csv':
            self.set_header('Conent-Type', 'application/json')
            self.write(res)


__all__ = ['get', 'put', 'post', 'patch', 'delete', 'head', 'RestfulMetaType', 'RestfulHandler']
