from medusa_protocol.binary.BinaryRequest import BinaryRequest
from medusa_protocol.binary.BinaryResponse import BinaryResponse

from medusa_network.Router import Router


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
