from dataclasses import is_dataclass
from unittest import TestCase, mock
from os import environ as env
import json

from requests.exceptions import HTTPError
from werkzeug.wrappers import Response
from jsonrpc import dispatcher
from arrow import get as _

from tokko_rpc import client as rpc_client
from tokko_rpc import server

RPC_HOST = "awesome.host"
RPC_PORT = "1234"
RPC_URL_SCHEMA = "https"


class ServerTestSuite(TestCase):

    def setUp(self) -> None:
        self.default_server_methods = ['status', 'ping', 'echo', 'methods']
        self.server_info = server.server_info

    def test_01_server_info(self):
        info = self.server_info()
        self.assertEqual(type(info), dict)
        self.assertEqual(
            _(info["started"]).format("YYYY-MM-DD HH:mm:ss"),
            _(server.started_at).format("YYYY-MM-DD HH:mm:ss")
        )
        self.assertEqual(
            info["meta"],
            {
                'version': '0.0.1',
                'codeName': 'Desperado'
            }
        )

    def test_02_setup_default_methods(self):
        # Before setup default methods
        info = self.server_info()
        self.assertEqual(info["methods"], [])
        server.setup_default_methods()
        # After methods population
        info = self.server_info()
        self.assertEqual(info["methods"], self.default_server_methods)
        self.assertEqual(sorted(list(dispatcher.keys())),
                         sorted(info["methods"]))

    def test_03_formatted_error_response(self):
        error = server.formatted_error_response(
            Exception("Some error"),
            status=500
        )
        self.assertEqual(type(error), Response)
        self.assertEqual(error.status_code, 500)
        self.assertEqual(error.content_type, "application/json")
        self.assertEqual(error.data, json.dumps(
            {
                "id": None,
                "jsonrpc": "2.0",
                "result": None,
                "error":
                    {
                        "message": "Some error",
                        "code": 500
                    }
            }).encode())


class FakeResponse:

    def __init__(self, data, status_code: int = 200):
        self.__data__ = data
        self.__status_code__ = status_code

    def raise_for_status(self):
        if not self.status_code() == 200:
            raise HTTPError(f"Error. Code: {self.status_code()}")

    @classmethod
    def new(cls, data, status_code):
        return FakeResponse(data, status_code)

    def status_code(self):
        return self.__status_code__

    @property
    def text(self):
        return json.dumps(self.json())

    def json(self):
        return self.__data__


MOCKED_URLS = {
    f"{RPC_URL_SCHEMA}://{RPC_HOST}:{RPC_PORT}": {
        "data": {
            "jsonrpc": "2.0",
            "result": ["methods", "list"],
            "id": 1
        },
        "status": 200
    }
}


def mocked_requests_post(url, *args, **kwargs):
    try:
        return FakeResponse(data=MOCKED_URLS[url]["data"],
                            status_code=MOCKED_URLS[url]["status"])
    except KeyError:
        raise AttributeError(f"No mock for URL={url}")


class ClientTestSuite(TestCase):

    def setUp(self) -> None:
        env["RPC_GATEWAY_URL_HOST"] = self.host = RPC_HOST
        env["RPC_GATEWAY_URL_PORT"] = self.port = RPC_PORT
        env["RPC_GATEWAY_URL_SCHEMA"] = self.schema = RPC_URL_SCHEMA

    def test_01_the_client_class(self):
        client_class = rpc_client.Client
        self.assertEqual(is_dataclass(client_class), True)

    def test_02_the_instance_client(self):
        client = rpc_client.Client()
        self.assertEqual(client.host, self.host)
        self.assertEqual(client.port, self.port)
        self.assertEqual(client.schema, self.schema)

    def test_03_client_invalid_schema(self):
        with self.assertRaises(ValueError):
            rpc_client.Client(schema="invalid")

    def test_04_client_info(self):
        client = rpc_client.Client()
        self.assertEqual(client.server_url, f"{self.schema}://{self.host}:{self.port}")

    @mock.patch("requests.post", side_effect=mocked_requests_post)
    def test_05_client_common_functions_get_methods_list(self, get_mock):
        client = rpc_client.Client()
        self.assertEqual(client.local.methods(), ["methods", "list"])
