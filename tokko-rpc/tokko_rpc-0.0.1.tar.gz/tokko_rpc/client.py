from dataclasses import dataclass
from os import environ as env
import logging
import json

import requests
from requests.exceptions import (
    TooManyRedirects,
    ConnectionError,
    HTTPError,
    Timeout,
)
from tokko_rpc.exceptions import (
    ClientMisconfiguration
)

log = logging.getLogger(__name__)


@dataclass(init=True)
class Client:

    host: str = None
    port: int = None
    schema: str = None
    defaults_are_enabled: bool = True

    ALLOWED_SCHEMAS = ["http", "https"]
    __status__ = None
    __conn__ = None

    @dataclass
    class Remote:
        url: str
        service: str
        request_id: str = "1"

        @staticmethod
        def compile_inputs(*args, **kwargs) -> list:
            args = list(args)
            if kwargs:
                args += [(k, v) for k, v in kwargs.items()]
            return args

        def build_request(self, method, *args, **kwargs):
            payload = {
                "jsonrpc": "2.0",
                "method": method,
                "id": self.request_id,
                "params": self.compile_inputs(*args, **kwargs)
            }
            return self.call(self.service, payload)

        def call(self, service, payload):
            _url = self.url
            if service not in ["local"]:
                _url += f"/{service}"
            try:
                response = requests.post(_url, json=payload)
                if not response.status_code == 200:
                    raise response.raise_for_status()

                response = response.json()
                try:
                    return response["result"]
                except KeyError:
                    err = response["error"]
                    try:
                        err = err["data"]["message"]
                    except (KeyError, TypeError):
                        ...
                    raise ValueError(err)
            except (ConnectionError, Timeout, TooManyRedirects):
                raise IOError(f"Service {service}[{_url}] did not respond.")
            except HTTPError as content_error:
                # Yes... horrible
                if "404" in f"{content_error}":
                    content_error = "Request method not found"
                elif "400" in f"{content_error}":
                    content_error = "Bad params"
                else:
                    content_error = "Internal error"
                raise TypeError(f"{content_error}")
            except Exception as e:
                raise Exception(f"{e}'")

        def __getattr__(self, item):
            return lambda *a, **kw: self.build_request(item, *a, **kw)

    @property
    def server_url(self):
        return f"{self.schema}://{self.host}:{self.port}"

    @property
    def status(self):
        return self.__status__

    @property
    def connection(self):
        return self.__conn__

    def __set_defaults__(self):
        if not all([self.host, self.port, self.schema]) and not self.defaults_are_enabled:
            raise ClientMisconfiguration()
        self.host = self.host or env.get("RPC_GATEWAY_URL_HOST", "localhost")
        self.port = self.port or env.get("RPC_GATEWAY_URL_PORT", "4000")
        self.schema = self.schema or env.get("RPC_GATEWAY_URL_SCHEMA", "http")

    def __post_init__(self):
        self.__set_defaults__()
        if self.schema not in self.ALLOWED_SCHEMAS:
            raise ValueError("Unsupported schema")

    def __getattr__(self, item):
        conn = self.Remote(url=self.server_url, request_id="666", service=item)
        return conn
