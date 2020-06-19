import ipaddress
import shutil
from typing import List


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


async def load_scutil_dns(hub):
    scutil = shutil.which("scutil")
    if scutil:
        result = (await hub.exec.cmd.run([scutil, "--dns"])).stdout
        dns = {}

        # Parse the scutil output
        resolver = 0
        for line in result.splitlines():
            line = line.strip()
            if line.startswith("resolver"):
                resolver = int(line.split("#")[1])
                dns[resolver] = {}
            elif "[" in line and "]" in line:
                # "domain" and "nameserver" should show up here
                key = line.split("[")[0].strip()
                if key not in dns[resolver]:
                    dns[resolver][key] = []
                dns[resolver][key].append(line.split(":", maxsplit=2)[1].strip())
            elif ":" in line:
                key, value = line.split(":", maxsplit=2)
                key = key.strip()
                value = value.strip()
                # Normalize the scutil output
                if key in ("flags", "options"):
                    value = {x.strip() for x in value.split(",")}
                elif key in ("order", "timeout"):
                    value = int(value)
                elif key == "reach":
                    value = "Not Reachable" not in value
                dns[resolver][key] = value

        # Parse reachable resolvers
        flags = set()
        nameservers = []
        options = set()
        domain = []
        for x in dns.values():
            if x.get("reach"):
                nameservers.extend(x.get("nameserver", []))
                domain.extend(x.get("search domain", []))
                options.update(x.get("options", set()))
                flags.update(x.get("flags", set()))

        hub.grains.GRAINS.dns.flags = sorted(flags)
        hub.grains.GRAINS.dns.nameservers = nameservers
        hub.grains.GRAINS.dns.options = sorted(options)
        hub.grains.GRAINS.dns.domain = domain
        hub.grains.GRAINS.dns.search = []
        hub.grains.GRAINS.dns.sortlist = (
            await _get_sortlist(hub.grains.GRAINS.dns.nameservers) or []
        )
        hub.grains.GRAINS.dns.ip4_nameservers = [
            ip for ip in hub.grains.GRAINS.dns.nameservers if await _is_ipv4_address(ip)
        ]

        hub.grains.GRAINS.dns.ip6_nameservers = [
            ip for ip in hub.grains.GRAINS.dns.nameservers if await _is_ipv6_address(ip)
        ]
