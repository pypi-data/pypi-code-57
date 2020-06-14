from werkzeug.exceptions import HTTPException
from werkzeug.serving import run_simple
from .router import Router
from .request import Request
from .response import Response
from injector import inject


class HttpKernel:
    @inject
    def __init__(self, router: Router):
        self.router = router

    def dispatch_request(self, request):
        adapter = self.router.routers_map.bind_to_environ(request.environ)
        endpoint, values = adapter.match()
        values["request"] = request
        response = endpoint(**values)
        if not isinstance(response, Response):
            response = self._create_response(response)
        return response

    def wsgi_app(self, environ, start_response):
        request = self._create_request(environ)
        try:
            response = self.dispatch_request(request)
            return response(environ, start_response)
        except HTTPException as e:
            return e

    def _create_response(self, response):
        return Response(response)

    def _create_request(self, environ):
        return Request(environ)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def default_config(self):
        return dict(
            hostname="0.0.0.0",
            port=8000,
            use_debugger=True,
            use_reloader=True,
            application=self,
        )

    def run(self, **kwargs):
        options = {**self.default_config(), **kwargs}
        run_simple(**options)
