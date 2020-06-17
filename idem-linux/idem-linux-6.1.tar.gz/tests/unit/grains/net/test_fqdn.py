import idem_linux.grains.net.fqdn
import pytest
import socket
import mock
from dict_tools import data


@pytest.mark.asyncio
async def test_load_socket_info(mock_hub):
    mock_hub.exec.cmd.run.return_value = data.NamespaceDict({"stdout": "test.local"})

    ret = (
        (()),
        (
            ({socket.AF_INET: 2}, {socket.SOCK_DGRAM: 2}, 17, "", ("127.0.0.1", 0)),
            ({socket.AF_INET: 2}, {socket.SOCK_STREAM: 1}, 6, "", ("127.0.0.1", 0)),
            ({socket.AF_INET: 2}, {socket.SOCK_DGRAM: 2}, 17, "", ("192.168.1.24", 0),),
            ({socket.AF_INET: 2}, {socket.SOCK_STREAM: 1}, 6, "", ("192.168.1.24", 0),),
        ),
        (
            ({socket.AF_INET6: 30}, {socket.SOCK_DGRAM: 2}, 17, "", ("::1", 0, 0, 0),),
            ({socket.AF_INET6: 30}, {socket.SOCK_STREAM: 1}, 6, "", ("::1", 0, 0, 0),),
            (
                {socket.AF_INET6: 30},
                {socket.SOCK_DGRAM: 2},
                17,
                "",
                ("fe80::1", 0, 0, 1),
            ),
            (
                {socket.AF_INET6: 30},
                {socket.SOCK_STREAM: 1},
                6,
                "",
                ("fe80::1", 0, 0, 1),
            ),
            (
                {socket.AF_INET6: 30},
                {socket.SOCK_DGRAM: 2},
                17,
                "",
                ("fe80::cac:ffff:ffff:ffff", 0, 0, 4),
            ),
            (
                {socket.AF_INET6: 30},
                {socket.SOCK_STREAM: 1},
                6,
                "",
                ("fe80::cac:ffff:ffff:ffff", 0, 0, 4),
            ),
        ),
    )
    with mock.patch.object(socket, "getfqdn", return_value="test.local"):
        with mock.patch.object(socket, "getaddrinfo", side_effect=ret):
            with mock.patch.object(socket, "gethostname", return_value="test_host"):
                await idem_linux.grains.net.fqdn.load_socket_info(mock_hub)

    assert mock_hub.grains.GRAINS.domain == "local"
    assert mock_hub.grains.GRAINS.fqdn == "test.local"
    assert mock_hub.grains.GRAINS.localhost == "test_host"

    # These ones require socket to be mocked
    assert mock_hub.grains.GRAINS.fqdn_ip4 == ("127.0.0.1", "192.168.1.24")
    assert mock_hub.grains.GRAINS.fqdn_ip6 == (
        "::1",
        "fe80::1",
        "fe80::cac:ffff:ffff:ffff",
    )
    assert mock_hub.grains.GRAINS.fqdns == (
        "127.0.0.1",
        "192.168.1.24",
        "::1",
        "fe80::1",
        "fe80::cac:ffff:ffff:ffff",
    )
