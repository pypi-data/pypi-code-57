from os import environ as env
from typing import Any
import logging
import json

from jsonrpc import JSONRPCResponseManager as JSONIOManager, dispatcher
from werkzeug.wrappers import Request, Response
from werkzeug.serving import make_server
from arrow import now
import coloredlogs


from tokko_rpc.templates import WORKER_SPLASH
from tokko_rpc.utils import render

log = logging.getLogger(__name__)
coloredlogs.install(logger=log)

__version__ = "0.0.1"
started_at = now()

HOST = env.get("RPC_PROVIDER_HOST", "localhost")
PORT = int(env.get("RPC_PROVIDER_PORT", "4000"))
SCHEMA = "https" if env.get("RPC_PROVIDER_USE_SSL") else "http"


def server_info() -> dict:
    return {
        "started": started_at.format("YYYY-MM-DD HH:mm:ssZZ"),
        "upTimeSeconds": (now() - started_at).total_seconds(),
        "meta": {
            "version": __version__,
            "codeName": "Desperado",
        },
        "methods": list(dispatcher.keys())
    }


def setup_default_methods():
    dispatcher.add_method(server_info, "status")
    dispatcher.add_method(lambda: "Pong!", "ping")
    dispatcher.add_method(lambda string: string, "echo")
    dispatcher.add_method(lambda: list(dispatcher.keys()), "methods")


def formatted_error_response(error: Any, status=500):
    return Response(json.dumps({
        "id": None,
        "jsonrpc": "2.0",
        "result": None,
        "error": {
            "message": f"{error}",
            "code": status
        }
    }), mimetype="application/json", status=status)


@Request.application
def _application_(request):
    try:
        result = JSONIOManager.handle(request.data, dispatcher)
        inflated = json.loads(result.json)
        try:
            if "not found" in inflated["error"]["message"]:
                return formatted_error_response(Exception("Method not found"), 404)
        except KeyError:
            ...
        response = Response(result.json, mimetype="application/json")
    except Exception as e:
        log.exception(e)
        return formatted_error_response(e, 400)
    return response


def create_application():
    setup_default_methods()
    return _application_


def build_server(host=None, port=None, schema=None, splash=None):
    if not splash:
        splash = render(
            WORKER_SPLASH,
            **dict(host=host or HOST,
                   port=port or PORT,
                   version=__version__,
                   schema=schema or SCHEMA,
                   started_at=started_at.format("YY-MM-DD HH:mm:ssZZ"))
        )
    print(splash, flush=True)
    return make_server(host, port, create_application())
