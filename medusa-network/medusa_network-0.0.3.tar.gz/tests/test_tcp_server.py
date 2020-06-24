import asyncio

import pytest
from medusa_protocol import BinaryRequest, BinaryResponse

from medusa_network import Router, TcpServer, TcpClient


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
        TcpServer(router=router, address="::", port=5060)
    ]


@pytest.fixture
async def client() -> TcpClient:
    reader, writer = await asyncio.open_connection("localhost", 5060)
    client: TcpClient = TcpClient(reader, writer)
    return client


async def test_tcp_server(client):
    # call the client
    request_client: BinaryRequest = BinaryRequest()
    request_client.action = "echo"
    request_client.body = "this is a test"
    response: BinaryResponse = await client.send(request_client)
    await client.close()
    assert "this is a test" == response.body
