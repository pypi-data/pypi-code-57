import shutil


async def load_default_gateway(hub):
    """
    Populates grains which describe whether a server has a default gateway
    configured or not. Uses `ip -4 route show` and `ip -6 route show` and greps
    for a `default` at the beginning of any line. Assuming the standard
    `default via <ip>` format for default gateways, it will also parse out the
    ip address of the default gateway, and put it in ip4_gw or ip6_gw.

    If the `ip` command is unavailable, no grains will be populated.

    Currently does not support multiple default gateways. The grains will be
    set to the first default gateway found.

    List of grains:

        ip4_gw: True  # ip/True/False if default ipv4 gateway
        ip6_gw: True  # ip/True/False if default ipv6 gateway
        ip_gw: True   # True if either of the above is True, False otherwise
    """
    ip_bin = shutil.which("ip")
    if ip_bin:
        hub.grains.GRAINS.ip4_gw = False
        hub.grains.GRAINS.ip6_gw = False
        for ip_version in (4, 6):
            try:
                out = (
                    await hub.exec.cmd.run([ip_bin, f"-{ip_version}", "route", "show"])
                ).stdout.strip()
                for line in out.splitlines():
                    if line.startswith("default"):
                        hub.grains.GRAINS[f"ip{ip_version}_gw"] = True
                        try:
                            via, gw_ip = line.split()[1:3]
                        except ValueError:
                            pass
                        else:
                            if via == "via":
                                hub.grains.GRAINS[f"ip{ip_version}_gw"] = gw_ip
                        break
            except Exception:  # pylint: disable=broad-except
                continue

        hub.grains.GRAINS.ip_gw = bool(hub.grains.GRAINS.ip4_gw) or bool(
            hub.grains.GRAINS.ip6_gw
        )
