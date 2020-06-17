import idem_linux.grains.net.interfaces
import pytest
import shutil
import mock
from dict_tools import data

IP_LINK_DATA = """
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: wlp59s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DORMANT group default qlen 1000
    link/ether 9c:b6:d0:c4:71:ab brd ff:ff:ff:ff:ff:ff
3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT group default
    link/ether 02:42:6a:d9:ec:5e brd ff:ff:ff:ff:ff:ff
"""

IP_ADDR_DATA = """
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: wlp59s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 9c:b6:d0:c4:71:ab brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.27/24 brd 192.168.1.255 scope global dynamic noprefixroute wlp59s0
       valid_lft 81422sec preferred_lft 81422sec
    inet6 fe80::adaf:ffff:ffff:ffff/64 scope link noprefixroute
       valid_lft forever preferred_lft forever
3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default
    link/ether 02:42:6a:d9:ec:5e brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
       valid_lft forever preferred_lft forever
"""

IFCONFIG_DATA = """
docker0: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        inet 172.17.0.1  netmask 255.255.0.0  broadcast 172.17.255.255
        ether 02:42:6a:d9:ec:5e  txqueuelen 0  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 23967  bytes 2072902 (1.9 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 23967  bytes 2072902 (1.9 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

wlp59s0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.27  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::adaf:ffff:ffff:ffff  prefixlen 64  scopeid 0x20<link>
        ether 9c:b6:d0:c4:71:ab  txqueuelen 1000  (Ethernet)
        RX packets 3212223  bytes 2478150420 (2.3 GiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 1877277  bytes 669252923 (638.2 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
"""


@pytest.mark.asyncio
async def test_load_interfaces_ip(mock_hub):
    mock_hub.exec.cmd.run.side_effect = [
        data.NamespaceDict({"stdout": IP_LINK_DATA}),
        data.NamespaceDict({"stdout": IP_ADDR_DATA}),
    ]
    with mock.patch.object(shutil, "which", side_effect=[True, False]):
        await idem_linux.grains.net.interfaces.load_interfaces(mock_hub)

    assert mock_hub.grains.GRAINS.hwaddr_interfaces._dict() == {
        "docker0": "02:42:6a:d9:ec:5e",
        "lo": "00:00:00:00:00:00",
        "wlp59s0": "9c:b6:d0:c4:71:ab",
    }
    assert mock_hub.grains.GRAINS.ip4_interfaces._dict() == {
        "docker0": ("172.17.0.1",),
        "lo": ("127.0.0.1",),
        "wlp59s0": ("192.168.1.27",),
    }
    assert mock_hub.grains.GRAINS.ip6_interfaces._dict() == {
        "lo": ("::1",),
        "wlp59s0": ("fe80::adaf:ffff:ffff:ffff",),
    }
    assert mock_hub.grains.GRAINS.ip_interfaces._dict() == {
        "docker0": ("172.17.0.1",),
        "lo": ("127.0.0.1", "::1"),
        "wlp59s0": ("192.168.1.27", "fe80::adaf:ffff:ffff:ffff"),
    }
    assert mock_hub.grains.GRAINS.ipv4 == ("127.0.0.1", "172.17.0.1", "192.168.1.27")
    assert mock_hub.grains.GRAINS.ipv6 == ("::1", "fe80::adaf:ffff:ffff:ffff")


@pytest.mark.asyncio
async def test_load_interfaces_ifconfig(mock_hub):
    mock_hub.exec.cmd.run.return_value = data.NamespaceDict({"stdout": IFCONFIG_DATA})
    with mock.patch.object(shutil, "which", side_effect=[False, True]):
        await idem_linux.grains.net.interfaces.load_interfaces(mock_hub)

    assert mock_hub.grains.GRAINS.hwaddr_interfaces._dict() == {
        "docker0": "02:42:6a:d9:ec:5e",
        # "lo": "00:00:00:00:00:00",
        "wlp59s0": "9c:b6:d0:c4:71:ab",
    }
    assert mock_hub.grains.GRAINS.ip4_interfaces._dict() == {
        "docker0": ("172.17.0.1",),
        "lo": ("127.0.0.1",),
        "wlp59s0": ("192.168.1.27",),
    }
    assert mock_hub.grains.GRAINS.ip6_interfaces._dict() == {
        "lo": ("::1",),
        "wlp59s0": ("fe80::adaf:ffff:ffff:ffff",),
    }
    assert mock_hub.grains.GRAINS.ip_interfaces._dict() == {
        "docker0": ("172.17.0.1",),
        "lo": ("127.0.0.1", "::1"),
        "wlp59s0": ("192.168.1.27", "fe80::adaf:ffff:ffff:ffff"),
    }
    assert mock_hub.grains.GRAINS.ipv4 == ("127.0.0.1", "172.17.0.1", "192.168.1.27")
    assert mock_hub.grains.GRAINS.ipv6 == ("::1", "fe80::adaf:ffff:ffff:ffff")
