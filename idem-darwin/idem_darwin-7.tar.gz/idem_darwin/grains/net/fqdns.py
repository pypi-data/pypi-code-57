import shutil
import socket
from typing import List


async def _get_fqdns(fqdn: str, protocol: int) -> List[str]:
    default = socket.getdefaulttimeout()
    socket.setdefaulttimeout(1)
    try:
        result = socket.getaddrinfo(fqdn, None, protocol)
        return sorted({item[4][0] for item in result})
    except socket.gaierror as e:
        hub.log.debug(e)
    socket.setdefaulttimeout(default)
    return []


async def load_fqdns(hub):
    scutil = shutil.which("scutil")
    if scutil:
        hub.grains.GRAINS.localhost = (
            await hub.exec.cmd.run([scutil, "--get", "LocalHostName"])
        ).stdout.strip()
        hostname = shutil.which("hostname")
        if hostname:
            hub.grains.GRAINS.fqdn = (
                await hub.exec.cmd.run([hostname, "-f"])
            ).stdout.strip()

            hub.log.debug("loading fqdns based grains")
            (
                hub.grains.GRAINS.host,
                hub.grains.GRAINS.domain,
            ) = hub.grains.GRAINS.fqdn.partition(".")[::2]
            if not hub.grains.GRAINS.domain:
                hub.grains.GRAINS.domain = "local"
                hub.grains.GRAINS.fqdn += ".local"
            if "." not in hub.grains.GRAINS.localhost:
                hub.grains.GRAINS.localhost += f".{hub.grains.GRAINS.domain}"
            hub.grains.GRAINS.fqdn_ip4 = await _get_fqdns(
                hub.grains.GRAINS.fqdn, socket.AF_INET
            )
            hub.grains.GRAINS.fqdn_ip6 = await _get_fqdns(
                hub.grains.GRAINS.fqdn, socket.AF_INET6
            )
            hub.grains.GRAINS.fqdns = (
                hub.grains.GRAINS.fqdn_ip4 + hub.grains.GRAINS.fqdn_ip6
            )
