import ifcfg


async def load_interfaces(hub):
    """
    Provide a dict of the connected interfaces and their ip addresses
    The addresses will be passed as a list for each interface
    """
    ipv4 = set()
    ipv6 = set()
    ifconfig = ifcfg.parser.UnixParser()

    for interface, device in sorted(ifconfig.interfaces.items()):
        hw_addr = device.get("ether")
        if hw_addr:
            hub.grains.GRAINS.hwaddr_interfaces[interface] = hw_addr
        ipv4.update(device["inet4"])
        if device["inet4"]:
            hub.grains.GRAINS.ip4_interfaces[interface] = sorted(device["inet4"])
        ipv6.update(device["inet6"])
        if device["inet6"]:
            hub.grains.GRAINS.ip6_interfaces[interface] = sorted(device["inet6"])

        hub.grains.GRAINS.ip_interfaces[interface] = sorted(device["inet4"]) + sorted(
            device["inet6"]
        )

    hub.grains.GRAINS.ipv4 = sorted(ipv4)
    hub.grains.GRAINS.ipv6 = sorted(ipv6)
