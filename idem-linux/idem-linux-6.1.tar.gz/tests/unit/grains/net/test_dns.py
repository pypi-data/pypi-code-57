import dns.resolver
import idem_linux.grains.net.dns
import io
import pytest
import mock

RESOLV_CONF = """
domain test.domain
options rotate timeout:1 retries:1
search example.com company.net
nameserver 10.0.0.1
nameserver 10.0.0.2
nameserver fe80::1
"""


@pytest.mark.asyncio
async def test_load_dns(mock_hub):
    mocK_resolv = dns.resolver.Resolver(io.StringIO(RESOLV_CONF), configure=True)
    mocK_resolv.read_resolv_conf = lambda x: 0

    with mock.patch.object(dns.resolver, "Resolver", return_value=mocK_resolv):
        await idem_linux.grains.net.dns.load_dns(mock_hub)

    assert mock_hub.grains.GRAINS.dns.nameservers == ("10.0.0.1", "10.0.0.2", "fe80::1")
    assert mock_hub.grains.GRAINS.dns.ip4_nameservers == ("10.0.0.1", "10.0.0.2")
    assert mock_hub.grains.GRAINS.dns.ip6_nameservers == ("fe80::1",)
    assert mock_hub.grains.GRAINS.dns.sortlist == (
        "10.0.0.0/8",
        "10.0.0.0/8",
        "fe80::1/128",
    )
    assert mock_hub.grains.GRAINS.dns.domain == "test.domain."
    assert mock_hub.grains.GRAINS.dns.search == ("example.com.", "company.net.")
    assert mock_hub.grains.GRAINS.dns.options.rotate is True
