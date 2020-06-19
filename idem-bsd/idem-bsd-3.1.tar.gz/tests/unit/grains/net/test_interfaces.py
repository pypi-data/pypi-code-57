import ifcfg
import pytest
import mock

IFCONFIG_DATA = """
lo0: flags=8049<UP,LOOPBACK,RUNNING,MULTICAST> mtu 16384
	options=1203<RXCSUM,TXCSUM,TXSTATUS,SW_TIMESTAMP>
	inet 127.0.0.1 netmask 0xff000000
	inet6 ::1 prefixlen 128
	inet6 fe80::1%lo0 prefixlen 64 scopeid 0x1
	nd6 options=201<PERFORMNUD,DAD>
gif0: flags=8010<POINTOPOINT,MULTICAST> mtu 1280
stf0: flags=0<> mtu 1280
en0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
	options=400<CHANNEL_IO>
	ether 88:e9:fe:ff:ff:ff
	inet6 fe80::cac:ffff:ffff:ffff%en0 prefixlen 64 secured scopeid 0x4
	inet 192.168.1.24 netmask 0xffffff00 broadcast 192.168.1.255
	nd6 options=201<PERFORMNUD,DAD>
	media: autoselect
	status: active
en1: flags=8963<UP,BROADCAST,SMART,RUNNING,PROMISC,SIMPLEX,MULTICAST> mtu 1500
	options=460<TSO4,TSO6,CHANNEL_IO>
	ether 82:37:64:ff:ff:ff
	media: autoselect <full-duplex>
	status: inactive
en2: flags=8963<UP,BROADCAST,SMART,RUNNING,PROMISC,SIMPLEX,MULTICAST> mtu 1500
	options=460<TSO4,TSO6,CHANNEL_IO>
	ether 82:37:64:ff:ff:ff
	media: autoselect <full-duplex>
	status: inactive
bridge0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
	options=63<RXCSUM,TXCSUM,TSO4,TSO6>
	ether 82:37:64:ff:ff:ff
	Configuration:
		id 0:0:0:0:0:0 priority 0 hellotime 0 fwddelay 0
		maxage 0 holdcnt 0 proto stp maxaddr 100 timeout 1200
		root id 0:0:0:0:0:0 priority 0 ifcost 0 port 0
		ipfilter disabled flags 0x0
	member: en1 flags=3<LEARNING,DISCOVER>
	        ifmaxaddr 0 port 5 priority 0 path cost 0
	member: en2 flags=3<LEARNING,DISCOVER>
	        ifmaxaddr 0 port 6 priority 0 path cost 0
	nd6 options=201<PERFORMNUD,DAD>
	media: <unknown type>
	status: inactive
p2p0: flags=8843<UP,BROADCAST,RUNNING,SIMPLEX,MULTICAST> mtu 2304
	options=400<CHANNEL_IO>
	ether 0a:e9:fe:ff:ff:ff
	media: autoselect
	status: inactive
awdl0: flags=8943<UP,BROADCAST,RUNNING,PROMISC,SIMPLEX,MULTICAST> mtu 1484
	options=400<CHANNEL_IO>
	ether ca:59:e0:ff:ff:ff
	inet6 fe80::c859:ffff:ffff:ffff%awdl0 prefixlen 64 scopeid 0x9
	nd6 options=201<PERFORMNUD,DAD>
	media: autoselect
	status: active
llw0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
	options=400<CHANNEL_IO>
	ether ca:59:e0:ff:ff:ff
	inet6 fe80::c859:ffff:ffff:ffff%llw0 prefixlen 64 scopeid 0xa
	nd6 options=201<PERFORMNUD,DAD>
	media: autoselect
	status: active
utun0: flags=8051<UP,POINTOPOINT,RUNNING,MULTICAST> mtu 1380
	inet6 fe80::34f5:ffff:ffff:ffff%utun0 prefixlen 64 scopeid 0xb
	nd6 options=201<PERFORMNUD,DAD>
utun1: flags=8051<UP,POINTOPOINT,RUNNING,MULTICAST> mtu 2000
	inet6 fe80::7eaf:ffff:ffff:ffff%utun1 prefixlen 64 scopeid 0xc
	nd6 options=201<PERFORMNUD,DAD>
"""


@pytest.mark.asyncio
async def test_load_interfaces(mock_hub, hub):

    with mock.patch.object(
        ifcfg.parser,
        "UnixParser",
        return_value=ifcfg.parser.UnixParser(ifconfig=IFCONFIG_DATA),
    ):
        mock_hub.grains.net.interfaces.load_interfaces = (
            hub.grains.net.interfaces.load_interfaces
        )
        await mock_hub.grains.net.interfaces.load_interfaces()

    assert mock_hub.grains.GRAINS.hwaddr_interfaces == {
        "awdl0": "ca:59:e0:ff:ff:ff",
        "bridge0": "82:37:64:ff:ff:ff",
        "en0": "88:e9:fe:ff:ff:ff",
        "en1": "82:37:64:ff:ff:ff",
        "en2": "82:37:64:ff:ff:ff",
        "llw0": "ca:59:e0:ff:ff:ff",
        "p2p0": "0a:e9:fe:ff:ff:ff",
    }
    assert mock_hub.grains.GRAINS.ip4_interfaces == {
        "en0": ("192.168.1.24",),
        "lo0": ("127.0.0.1",),
    }
    assert mock_hub.grains.GRAINS.ip6_interfaces == {
        "awdl0": ("fe80::c859:ffff:ffff:ffff",),
        "en0": ("fe80::cac:ffff:ffff:ffff",),
        "llw0": ("fe80::c859:ffff:ffff:ffff",),
        "lo0": ("::1", "fe80::1"),
        "utun0": ("fe80::34f5:ffff:ffff:ffff",),
        "utun1": ("fe80::7eaf:ffff:ffff:ffff",),
    }
    assert mock_hub.grains.GRAINS.ip_interfaces._dict() == {
        "awdl0": ("fe80::c859:ffff:ffff:ffff",),
        "bridge0": (),
        "en0": ("192.168.1.24", "fe80::cac:ffff:ffff:ffff"),
        "en1": (),
        "en2": (),
        "gif0": (),
        "llw0": ("fe80::c859:ffff:ffff:ffff",),
        "lo0": ("127.0.0.1", "::1", "fe80::1"),
        "p2p0": (),
        "stf0": (),
        "utun0": ("fe80::34f5:ffff:ffff:ffff",),
        "utun1": ("fe80::7eaf:ffff:ffff:ffff",),
    }

    assert mock_hub.grains.GRAINS.ipv4 == ("127.0.0.1", "192.168.1.24")
    assert mock_hub.grains.GRAINS.ipv6 == (
        "::1",
        "fe80::1",
        "fe80::34f5:ffff:ffff:ffff",
        "fe80::7eaf:ffff:ffff:ffff",
        "fe80::c859:ffff:ffff:ffff",
        "fe80::cac:ffff:ffff:ffff",
    )
