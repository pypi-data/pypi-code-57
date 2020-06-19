import shutil


async def load_default_gateway(hub):
    """
    Populates grains which describe whether a server has a default gateway
    configured or not. Uses `ip -4 route show` and `ip -6 route show` and greps
    for a `default` at the beginning of any line. Assuming the standard
    `default via <ip>` format for default gateways, it will also parse out the
    ip address of the default gateway, and put it in ip4_gw or ip6_gw.

    If the `ifconfig` command is unavailable, no grains will be populated.

    List of grains:

        ip4_gw: True  # ip/True/False if default ipv4 gateway
        ip6_gw: True  # ip/True/False if default ipv6 gateway
        ip_gw: True   # True if either of the above is True, False otherwise
    """
    ip_gw_addr = {4: set(), 6: set()}
    ip_gw = {4: False, 6: False}

    netstat = shutil.which("netstat")
    if netstat:
        for ip_version in (4, 6):
            out = (
                await hub.exec.cmd.run(
                    [netstat, "-nrlf", "inet" if ip_version == 4 else "inet6"]
                )
            ).stdout.strip()
            for line in out.splitlines():
                if line.startswith("default"):
                    ip_gw[ip_version] = True
                    ip_gw_addr[ip_version].add(line.split()[1])

    hub.grains.GRAINS.ip4_gw = sorted(ip_gw_addr[4]) or ip_gw[4] or False
    hub.grains.GRAINS.ip6_gw = sorted(ip_gw_addr[6]) or ip_gw[6] or False
    hub.grains.GRAINS.ip_gw = bool(hub.grains.GRAINS.ip4_gw or hub.grains.GRAINS.ip6_gw)
