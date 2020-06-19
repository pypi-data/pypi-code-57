import dns.resolver

import ipaddress
from typing import Any, Dict, List


async def _cidr_to_ipv4_netmask(cidr_bits: str or int) -> str:
    """
    Returns an IPv4 netmask
    """
    try:
        cidr_bits = int(cidr_bits)
        if not 1 <= cidr_bits <= 32:
            return ""
    except ValueError:
        return ""

    netmask = ""
    for idx in range(4):
        if idx:
            netmask += "."
        if cidr_bits >= 8:
            netmask += "255"
            cidr_bits -= 8
        else:
            netmask += "{0:d}".format(256 - (2 ** (8 - cidr_bits)))
            cidr_bits = 0
    return netmask


async def _ipv4_to_bits(ipaddr: str) -> str:
    """
    Accepts an IPv4 dotted quad and returns a string representing its binary
    counterpart
    """
    return "".join([bin(int(x))[2:].rjust(8, "0") for x in ipaddr.split(".")])


async def _natural_ipv4_netmask(ip_addr: str, fmt: str = "prefixlen") -> str:
    """
    Returns the "natural" mask of an IPv4 address
    """
    bits = await _ipv4_to_bits(ip_addr)

    if bits.startswith("11"):
        mask = "24"
    elif bits.startswith("1"):
        mask = "16"
    else:
        mask = "8"

    if fmt == "netmask":
        return await _cidr_to_ipv4_netmask(mask)
    else:
        return "/" + mask


async def _is_ipv4_address(ip: str) -> bool:
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False


async def _is_ipv6_address(ip: str) -> bool:
    try:
        ipaddress.IPv6Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False


async def _parse_options(options: Dict[str, Any]) -> Dict[str, Any]:
    ret = {}
    for key, value in options.items():
        if key.startswith("_"):
            continue
        elif value:
            if key == "keyalgorithm":
                ret[key] = str(value)
            elif key not in ("domain", "nameservers", "search"):
                ret[key] = value
    return ret


async def _get_sortlist(ip_addrs: List[str]) -> List[str]:
    ret = []
    for ip_raw in ip_addrs:
        try:
            ip_net = ipaddress.ip_network(ip_raw)
        except ValueError as exc:
            hub.log.error(exc)
        else:
            if "/" not in ip_raw:
                # No netmask has been provided, guess
                # the "natural" one
                if ip_net.version == 4:
                    ip_addr = str(ip_net.network_address)
                    # pylint: disable=protected-access
                    mask = await _natural_ipv4_netmask(ip_addr)
                    ip_net = ipaddress.ip_network(f"{ip_addr}{mask}", strict=False)
                if ip_net.version == 6:
                    # TODO
                    pass

            if ip_net not in ret:
                ret.append(str(ip_net))
    return ret


async def load_dns(hub):
    """
    Parse the resolver configuration file
    """
    resolv = dns.resolver.Resolver(configure=True, filename="")

    hub.grains.GRAINS.dns.nameservers = resolv.nameservers
    hub.grains.GRAINS.dns.ip4_nameservers = [
        ip for ip in resolv.nameservers if await _is_ipv4_address(ip)
    ]

    hub.grains.GRAINS.dns.ip6_nameservers = [
        ip for ip in resolv.nameservers if await _is_ipv6_address(ip)
    ]

    hub.grains.GRAINS.dns.sortlist = await _get_sortlist(resolv.nameservers)
    hub.grains.GRAINS.dns.domain = resolv.domain
    hub.grains.GRAINS.dns.search = resolv.search
    hub.grains.GRAINS.dns.options = await _parse_options(resolv.__dict__)
