from pathlib import Path
from typing import Callable, IO, Optional, Union

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse, Response
from starlette.routing import Route
import yaml

from spell.serving.exceptions import BadAPIResponse, InvalidServerConfiguration
from spell.serving.api import API
from spell.serving.types import APIResponse

READY_FILE = "/ready"


def make_api_route(func: Callable[[Request], APIResponse]) -> Callable[[Request], APIResponse]:
    async def endpoint(request: Request) -> Response:
        return wrap_response(await func(request))

    return endpoint


def wrap_response(response: APIResponse) -> Response:
    response, tasks = response
    if isinstance(response, bytes):
        return Response(content=response, media_type="application/octet-stream", background=tasks)
    elif isinstance(response, str):
        return PlainTextResponse(content=response, background=tasks)
    elif isinstance(response, Response):
        if tasks is not None and tasks.tasks:
            if response.background:
                response.background.tasks += tasks.tasks
            else:
                response.background = tasks
        return response
    else:
        try:
            return JSONResponse(response, background=tasks)
        except Exception as e:
            raise BadAPIResponse(
                "Invalid response. Return an object that is JSON-serializable (including its "
                "nested fields), a bytes object, a string, or a "
                "starlette.response.Response object"
            ) from e


def make_api(
    config: Union[bytes, IO[bytes], str, IO[str]],
    entrypoint: str,
    python_path: Optional[str] = None,
    classname: Optional[str] = None,
) -> API:
    entrypoint = Path(entrypoint)
    if entrypoint.is_file():
        api = API.from_file(entrypoint, classname=classname)
    elif entrypoint.is_dir():
        if not python_path:
            raise InvalidServerConfiguration(
                "Classpath must be provided if entrypoint is a directory"
            )
        api = API.from_module(entrypoint, python_path, classname=classname)
    else:
        raise InvalidServerConfiguration(
            f"Entrypoint {entrypoint} must be a either a file or directory"
        )
    api.initialize_predictor(yaml.safe_load(config))
    return api


def create_ready_file() -> None:
    open(READY_FILE, "a").close()


def make_app(api: API, debug: bool = False) -> Starlette:
    routes = [
        Route("/predict", make_api_route(api.predict), methods=["POST"]),
        Route("/health", make_api_route(api.health), methods=["GET"]),
    ]

    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
            allow_credentials=True,
        ),
        Middleware(GZipMiddleware),
    ]
    return Starlette(
        debug=debug, routes=routes, middleware=middleware, on_startup=[create_ready_file]
    )
