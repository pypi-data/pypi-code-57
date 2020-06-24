from functools import partial

import pytest
from medusa_protocol import BinaryRequest, BinaryResponse

from medusa_network import Router, UdpServer, UdpClient
from medusa_network.Utils import get_random_port


@pytest.fixture
def router():
    def test_echo(request: BinaryRequest) -> BinaryResponse:
        response = BinaryResponse()
        response.code = 200
        response.body = request.body
        return response

    router = Router()
    router.add("echo", test_echo)
    return router


@pytest.fixture
def services(router):
    return [
        UdpServer(router=router, address="127.0.0.1", port=16700)
    ]

@pytest.fixture
async def client(loop) -> UdpClient:
    random_port = get_random_port()
    transport, protocol = await loop.create_datagram_endpoint(
        UdpClient,
        local_addr=("127.0.0.1", random_port),
    )
    try:
        yield partial(protocol.send, ("127.0.0.1", 16700))
    finally:
        transport.close()


async def test_udp_server(client):
    request_client: BinaryRequest = BinaryRequest()
    request_client.action = "echo"
    request_client.body = "this is a test"
    response: BinaryResponse = await client(request_client)
    assert "this is a test" == response.body
