import idem_linux.grains.net.gateway
import pytest
import shutil
import mock
from dict_tools import data

IP4_DATA = """
default via 192.168.1.1 dev wlp59s0 proto dhcp metric 20600
172.17.0.0/16 dev docker0 proto kernel scope link src 172.17.0.1 linkdown
192.168.1.0/24 dev wlp59s0 proto kernel scope link src 192.168.1.27 metric 600
"""
IP6_DATA = """
::1 dev lo proto kernel metric 256 pref medium
fe80::/64 dev wlp59s0 proto kernel metric 600 pref medium
"""


@pytest.mark.asyncio
async def test_load_default_gateway(mock_hub):
    mock_hub.exec.cmd.run.side_effect = [
        data.NamespaceDict({"stdout": IP4_DATA}),
        data.NamespaceDict({"stdout": IP6_DATA}),
    ]

    with mock.patch.object(shutil, "which", return_value=True):
        await idem_linux.grains.net.gateway.load_default_gateway(mock_hub)

    assert mock_hub.grains.GRAINS.ip_gw is True
    assert mock_hub.grains.GRAINS.ip4_gw == "192.168.1.1"
    assert mock_hub.grains.GRAINS.ip6_gw is False
