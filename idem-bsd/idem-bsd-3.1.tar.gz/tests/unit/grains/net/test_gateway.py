from dict_tools import data
import pytest
import mock

NETSTAT_IP4_DATA = """
Routing tables

Internet:
Destination        Gateway            Flags     Netif Expire
default            192.168.1.1        UGS         em0
127.0.0.1          link#2             UH          lo0
192.168.1.0/24     link#1             U           em0
192.168.1.13       link#1             UHS         lo0
"""

NETSTAT_IP6_DATA = """
Internet6:
Destination                       Gateway                       Flags     Netif Expire
::/96                             ::1                           UGRS        lo0
::1                               link#2                        UH          lo0
::ffff:0.0.0.0/96                 ::1                           UGRS        lo0
fe80::/10                         ::1                           UGRS        lo0
fe80::%lo0/64                     link#2                        U           lo0
fe80::1%lo0                       link#2                        UHS         lo0
ff02::/16                         ::1                           UGRS        lo0
"""


@pytest.mark.asyncio
async def test_load_default_gateway(mock_hub, hub):
    mock_hub.exec.cmd.run.side_effect = [
        data.NamespaceDict({"stdout": NETSTAT_IP4_DATA}),
        data.NamespaceDict({"stdout": NETSTAT_IP6_DATA}),
    ]

    with mock.patch("shutil.which", return_value=True):
        mock_hub.grains.net.gateway.load_default_gateway = (
            hub.grains.net.gateway.load_default_gateway
        )
        await mock_hub.grains.net.gateway.load_default_gateway()

    assert mock_hub.grains.GRAINS.ip_gw is True
    assert mock_hub.grains.GRAINS.ip4_gw == "192.168.1.1"
    assert mock_hub.grains.GRAINS.ip6_gw is False
