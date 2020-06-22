from medusa_protocol.binary.BinaryRequest import BinaryRequest
from medusa_protocol.binary.BinaryResponse import BinaryResponse


def test_request():
    request = BinaryRequest()
    request.action = "test"
    request.body = "body test"
    encoded_request = request.encode()

    # import binary code
    imported_request = BinaryRequest()
    imported_request.decode(encoded_request)

    assert "test" == imported_request.action
    assert "body test" == imported_request.body


def test_response():
    response = BinaryResponse()
    response.code = 200
    response.body = "body test"
    encoded_response = response.encode()

    # import binary code
    imported_response = BinaryResponse()
    imported_response.decode(encoded_response)

    assert 200 == imported_response.code
    assert "body test" == imported_response.body
