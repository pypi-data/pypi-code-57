import ipaddress
from typing import Any, Dict, List


async def _get_interfaces(wmi_network_adapter_config: list,) -> Dict[str, any]:
    interfaces = {}
    for interface in wmi_network_adapter_config:
        interfaces[interface.description] = {}
        if interface.macaddress:
            interfaces[interface.description]["hwaddr"] = interface.macaddress
        if interface.ipenabled:
            interfaces[interface.description]["up"] = True
            for ip in interface.ipaddress:
                if "." in ip:
                    if "inet" not in interfaces[interface.description]:
                        interfaces[interface.description]["inet"] = []
                    item = {"address": ip, "label": interface.description}
                    if interface.defaultipgateway:
                        broadcast = next(
                            (i for i in interface.defaultipgateway if "." in i), ""
                        )
                        if broadcast:
                            item["broadcast"] = broadcast
                    if interface.ipsubnet:
                        netmask = next((i for i in interface.ipsubnet if "." in i), "")
                        if netmask:
                            item["netmask"] = netmask
                    interfaces[interface.description]["inet"].append(item)
                if ":" in ip:
                    if "inet6" not in interfaces[interface.description]:
                        interfaces[interface.description]["inet6"] = []
                    item = {"address": ip}
                    if interface.defaultipgateway:
                        interfaces[interface.description][
                            "defaultipgateway"
                        ] = interface.defaultipgateway
                        broadcast = next(
                            (i for i in interface.defaultipgateway if ":" in i), ""
                        )
                        if broadcast:
                            item["broadcast"] = broadcast
                    if interface.ipsubnet:
                        netmask = next((i for i in interface.ipsubnet if ":" in i), "")
                        if netmask:
                            item["netmask"] = netmask
                    interfaces[interface.description]["inet6"].append(item)
        else:
            interfaces[interface.description]["up"] = False
    return interfaces


async def load_interfaces(hub):
    """
    Obtain interface information for Windows systems
    Provides:
      ip_interfaces
    """
    ipv4 = []
    ipv6 = []
    ip4_gw = []
    ip6_gw = []
    interfaces = await _get_interfaces(
        await hub.exec.wmi.get("Win32_NetworkAdapterConfiguration", IPEnabled=1)
    )
    for interface, device in interfaces.items():
        hw_addr = device.get("hwaddr")
        if hw_addr:
            hub.grains.GRAINS.hwaddr_interfaces[interface] = hw_addr
        inet4: List[str] = [ip.get("address") for ip in device.get("inet", [])]
        ipv4.extend(inet4)
        if inet4:
            hub.grains.GRAINS.ip4_interfaces[interface] = inet4
        inet6: List[str] = [ip.get("address") for ip in device.get("inet6", [])]
        ipv6.extend(inet6)
        if inet6:
            hub.grains.GRAINS.ip6_interfaces[interface] = inet6
        hub.grains.GRAINS.ip_interfaces[interface] = inet4 + inet6

        # Load gateway
        for gateway in device.get("defaultipgateway", ()):
            addr = ipaddress.ip_address(gateway)
            if isinstance(addr, ipaddress.IPv4Address):
                ip4_gw.append(str(addr))
            elif isinstance(addr, ipaddress.IPv6Address):
                ip6_gw.append(str(addr))

    hub.grains.GRAINS.ip4_gw = ip4_gw or False
    hub.grains.GRAINS.ip6_gw = ip6_gw or False
    hub.grains.GRAINS.ip_gw = bool(ip4_gw or ip6_gw) or False

    hub.grains.GRAINS.ipv4 = ipv4
    hub.grains.GRAINS.ipv6 = ipv6
