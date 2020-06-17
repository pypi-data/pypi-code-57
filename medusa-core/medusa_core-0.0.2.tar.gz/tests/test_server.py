import pytest

from medusa_core.binary.BinaryRequest import BinaryRequest
from medusa_core.binary.BinaryResponse import BinaryResponse
from medusa_core.server.Router import Router
from medusa_core.server.TcpServer import TcpServer


@pytest.fixture
def router():
    def test_callback(request: BinaryRequest) -> BinaryResponse:
        response = BinaryResponse()
        response.code = 200
        response.body = "callback body"
        return response

    def test_callback_two(request: BinaryRequest) -> BinaryResponse:
        response = BinaryResponse()
        response.code = 200
        response.body = "callback again"
        return response

    router = Router()
    router.add("first", test_callback)
    router.add("second", test_callback_two)
    return router


@pytest.fixture
def services(router):
    return [
        TcpServer(router=router, address="127.0.0.1", port=5678)
    ]


def test_router():
    def test_callback(request: BinaryRequest) -> BinaryResponse:
        response = BinaryResponse()
        response.code = 200
        response.body = "callback body"
        return response

    def test_callback_two(request: BinaryRequest) -> BinaryResponse:
        response = BinaryResponse()
        response.code = 200
        response.body = "callback again"
        return response

    router = Router()
    router.add("first", test_callback)
    router.add("second", test_callback_two)
    callback = router.get("first")
    request = BinaryRequest()
    request.action = "ciao"

    callback_response: BinaryResponse = callback(request)
    assert callback_response.code == 200
    assert callback_response.body == "callback body"


def test_tcp_server():
    pass
