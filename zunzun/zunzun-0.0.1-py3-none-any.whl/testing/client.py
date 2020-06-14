from injector import Injector
from werkzeug.test import Client as BaseClient
from zunzun import HttpKernel
from werkzeug.wrappers import BaseResponse


class Client(BaseClient):
    @classmethod
    def create(cls, injector: Injector = None):
        if not injector:
            injector = Injector()
        http_kernel = injector.get(HttpKernel)
        return cls(http_kernel, BaseResponse)
