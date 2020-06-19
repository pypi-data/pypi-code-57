import shutil


async def load_default_gateway(hub):
    """
    Populates grains which describe whether a server has a default gateway
    configured or not. Uses `netstat -rn4 ` and `netstat -rn6` and looks
    for a `default` at the beginning of any line. Assuming the standard
    `default via <ip>` format for default gateways, it will also parse out the
    ip address of the default gateway, and put it in ip4_gw or ip6_gw.

    If the `netstat` command is unavailable, no grains will be populated.

    Currently does not support multiple default gateways. The grains will be
    set to the first default gateway found.

    List of grains:

        ip4_gw: True  # ip/True/False if default ipv4 gateway
        ip6_gw: True  # ip/True/False if default ipv6 gateway
        ip_gw: True   # True if either of the above is True, False otherwise
    """
    netstat = shutil.which("netstat")

    if netstat:
        for protocol in (4, 6):
            ret = await hub.exec.cmd.run(
                [netstat, "-r", "-f", "inet" if protocol is 4 else "inet6"]
            )
            for line in ret.stdout.splitlines():
                if line.startswith("default"):
                    hub.grains.GRAINS[f"ip{protocol}_gw"] = line.split()[1]
                    break
            else:
                hub.grains.GRAINS[f"ip{protocol}_gw"] = False

        hub.grains.GRAINS.ip_gw = bool(
            hub.grains.GRAINS.ip4_gw or hub.grains.GRAINS.ip6_gw
        )
