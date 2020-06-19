import socket
from typing import List


async def load_localhost(hub):
    hub.grains.GRAINS.localhost = socket.gethostname()


async def _get_fqdns(fqdn: str, protocol: int) -> List[str]:
    socket.setdefaulttimeout(1)
    try:
        result = socket.getaddrinfo(fqdn, None, protocol)
        return sorted({item[4][0] for item in result})
    except socket.gaierror as e:
        hub.log.debug(e)
    return []


async def load_fqdn(hub):
    # try socket.getaddrinfo to get fqdn
    try:
        addrinfo = socket.getaddrinfo(
            socket.gethostname(),
            0,
            socket.AF_UNSPEC,
            socket.SOCK_STREAM,
            socket.SOL_TCP,
            socket.AI_CANONNAME,
        )
        for info in addrinfo:
            # info struct [family, socktype, proto, canonname, sockaddr]
            if len(info) >= 4:
                hub.grains.GRAINS.fqdn = info[3]
    except socket.gaierror:
        pass

    if not hub.grains.GRAINS.get("fqdn"):
        hub.grains.GRAINS.fqdn = socket.getfqdn() or "localhost"

    hub.log.debug("loading host and domain")
    hub.grains.GRAINS.host, hub.grains.GRAINS.domain = hub.grains.GRAINS.fqdn.partition(
        "."
    )[::2]
    hub.log.debug("loading fqdns")
    hub.grains.GRAINS.fqdn_ip4 = await _get_fqdns(
        hub.grains.GRAINS.fqdn, socket.AF_INET
    )
    hub.grains.GRAINS.fqdn_ip6 = await _get_fqdns(
        hub.grains.GRAINS.fqdn, socket.AF_INET6
    )
    hub.grains.GRAINS.fqdns = hub.grains.GRAINS.fqdn_ip4 + hub.grains.GRAINS.fqdn_ip6
