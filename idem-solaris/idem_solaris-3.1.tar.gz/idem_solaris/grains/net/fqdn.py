import shutil
import socket
from typing import List


# Possible value for h_errno defined in netdb.h
HOST_NOT_FOUND = 1
NO_DATA = 4


async def _get_fqdns(fqdn: str, protocol: int) -> List[str]:
    try:
        result = socket.getaddrinfo(
            host=fqdn,
            port=None,
            family=protocol,
            proto=socket.IPPROTO_IP,
            flags=socket.AI_NUMERICSERV | socket.AI_ADDRCONFIG | socket.AI_PASSIVE,
        )
        return sorted({item[4][0] for item in result})
    except socket.gaierror as e:
        hub.log.debug(e)
    return []


async def load_socket_info(hub):
    hub.grains.GRAINS.localhost = socket.gethostname()

    hostname = shutil.which("hostname")
    if hostname:
        hub.grains.GRAINS.computer_name = (
            await hub.exec.cmd.run(hostname)
        ).stdout.strip()
        hub.grains.GRAINS.fqdn = (
            await hub.exec.cmd.run([hostname, "-f"])
        ).stdout.strip()
    else:
        hub.grains.GRAINS.computer_name = hub.grains.GRAINS.localhost

    # try socket.getaddrinfo to get fqdn
    try:
        addrinfo = socket.getaddrinfo(
            hub.grains.GRAINS.localhost,
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
        hub.grains.GRAINS.fqdn = socket.getfqdn()

    hub.grains.GRAINS.host, hub.grains.GRAINS.domain = hub.grains.GRAINS.fqdn.partition(
        "."
    )[::2]

    hub.grains.GRAINS.fqdn_ip4 = await _get_fqdns(
        hub.grains.GRAINS.fqdn, socket.AF_INET
    )
    hub.grains.GRAINS.fqdn_ip6 = await _get_fqdns(
        hub.grains.GRAINS.fqdn, socket.AF_INET6
    )
    hub.grains.GRAINS.fqdns = hub.grains.GRAINS.fqdn_ip4 + hub.grains.GRAINS.fqdn_ip6
