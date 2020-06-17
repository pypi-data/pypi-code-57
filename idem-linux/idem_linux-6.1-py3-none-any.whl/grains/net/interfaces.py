import asyncio

import re
import shutil
from typing import Any, Dict, List, Tuple


async def _cidr_to_ipv4_netmask(cidr_bits: int) -> str:
    """
    Returns an IPv4 netmask
    """
    try:
        cidr_bits = cidr_bits
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


async def _number_of_set_bits(x):
    """
    Returns the number of bits that are set in a 32bit int
    """
    # Taken from http://stackoverflow.com/a/4912729. Many thanks!
    x -= (x >> 1) & 0x55555555
    x = ((x >> 2) & 0x33333333) + (x & 0x33333333)
    x = ((x >> 4) + x) & 0x0F0F0F0F
    x += x >> 8
    x += x >> 16
    return x & 0x0000003F


async def _number_of_set_bits_to_ipv4_netmask(set_bits: int) -> str:
    """
    Returns an IPv4 netmask from the integer representation of that mask.

    Ex. 0xffffff00 -> '255.255.255.0'
    """
    return await _cidr_to_ipv4_netmask(await _number_of_set_bits(set_bits))


async def _interfaces_ifconfig(out: str) -> Dict[str, Any]:
    """
    Uses ifconfig to return a dictionary of interfaces with various information
    about each (up/down state, ip address, netmask, and hwaddr)
    """
    ret = {}

    piface = re.compile(r"^([^\s:]+)")
    pmac = re.compile(".*?(?:HWaddr|ether|address:|lladdr) ([0-9a-fA-F:]+)")
    pip = re.compile(r".*?(?:inet addr:|inet [^\d]*)(.*?)\s")
    pip6 = re.compile(".*?(?:inet6 addr: (.*?)/|inet6 )([0-9a-fA-F:]+)")
    pmask6 = re.compile(
        r".*?(?:inet6 addr: [0-9a-fA-F:]+/(\d+)|prefixlen (\d+))(?: Scope:([a-zA-Z]+)| scopeid (0x[0-9a-fA-F]))?"
    )
    pmask = re.compile(r".*?(?:Mask:|netmask )(?:((?:0x)?[0-9a-fA-F]{8})|([\d\.]+))")
    pupdown = re.compile("UP")
    pbcast = re.compile(r".*?(?:Bcast:|broadcast )([\d\.]+)")

    groups = re.compile("\r?\n(?=\\S)").split(out)
    for group in groups:
        data = {}
        iface = ""
        updown = False
        for line in group.splitlines():
            miface = piface.match(line)
            mmac = pmac.match(line)
            mip = pip.match(line)
            mip6 = pip6.match(line)
            mupdown = pupdown.search(line)
            if miface:
                iface = miface.group(1)
            if mmac:
                data["hwaddr"] = mmac.group(1)
            if mip:
                if "inet" not in data:
                    data["inet"] = list()
                addr_obj = dict()
                addr_obj["address"] = mip.group(1)
                mmask = pmask.match(line)
                if mmask:
                    if mmask.group(1):
                        mmask = await _number_of_set_bits_to_ipv4_netmask(
                            int(mmask.group(1), 16)
                        )
                    else:
                        mmask = mmask.group(2)
                    addr_obj["netmask"] = mmask
                mbcast = pbcast.match(line)
                if mbcast:
                    addr_obj["broadcast"] = mbcast.group(1)
                data["inet"].append(addr_obj)
            if mupdown:
                updown = True
            if mip6:
                if "inet6" not in data:
                    data["inet6"] = list()
                addr_obj = dict()
                addr_obj["address"] = mip6.group(1) or mip6.group(2)
                mmask6 = pmask6.match(line)
                if mmask6:
                    addr_obj["prefixlen"] = mmask6.group(1) or mmask6.group(2)
                    ipv6scope = mmask6.group(3) or mmask6.group(4)
                    addr_obj["scope"] = (
                        ipv6scope.lower() if ipv6scope is not None else ipv6scope
                    )
                    if addr_obj["address"] != "::" and addr_obj["prefixlen"] != 0:
                        data["inet6"].append(addr_obj)
        data["up"] = updown
        if iface in ret:
            # SunOS optimization, where interfaces occur twice in 'ifconfig -a'
            # output with the same name: for ipv4 and then for ipv6 addr family.
            # Every instance has it's own 'UP' status and we assume that ipv4
            # status determines global interface status.
            #
            # merge items with higher priority for older values
            # after that merge the inet and inet6 sub items for both
            ret[iface].update(data)
            if "inet" in data:
                ret[iface]["inet"].extend(
                    x for x in data["inet"] if x not in ret[iface]["inet"]
                )
            if "inet6" in data:
                ret[iface]["inet6"].extend(
                    x for x in data["inet6"] if x not in ret[iface]["inet6"]
                )
        else:
            ret[iface] = data
        del data
    return ret


async def _parse_network(
    type_: str, value: str, cols: Dict[str, Any]
) -> Tuple[str, int, str, str]:
    """
    Return a tuple of ip, netmask, broadcast
    based on the current set of cols
    """
    mask = None
    brd = None
    scope = None
    if "/" in value:  # we have a CIDR in this address
        ip, cidr = value.split("/")
    else:
        ip = value
        cidr = 32

    if type_ == "inet":
        mask = await _cidr_to_ipv4_netmask(int(cidr))
        if "brd" in cols:
            brd = cols[cols.index("brd") + 1]
    elif type_ == "inet6":
        mask = cidr
        if "scope" in cols:
            scope = cols[cols.index("scope") + 1]
    return ip, mask, brd, scope


async def _interfaces_ip(out: str) -> Dict[str, Any]:
    """
    Uses ip to return a dictionary of interfaces with various information about
    each (up/down state, ip address, netmask, and hwaddr)
    """
    ret = dict()

    groups = re.compile("\r?\n\\d").split(out)
    for group in groups:
        iface = None
        data = dict()

        for line in group.splitlines():
            if " " not in line:
                continue
            match = re.match(r"^\d*:\s+([\w.\-]+)(?:@)?([\w.\-]+)?:\s+<(.+)>", line)
            if match:
                iface, parent, attrs = match.groups()
                if "UP" in attrs.split(","):
                    data["up"] = True
                else:
                    data["up"] = False
                if parent:
                    data["parent"] = parent
                continue

            cols = line.split()
            if len(cols) >= 2:
                type_, value = tuple(cols[0:2])
                iflabel = cols[-1:][0]
                if type_ in ("inet", "inet6"):
                    if "secondary" not in cols:
                        ipaddr, netmask, broadcast, scope = await _parse_network(
                            type_, value, cols
                        )
                        if type_ == "inet":
                            if "inet" not in data:
                                data["inet"] = list()
                            addr_obj = dict()
                            addr_obj["address"] = ipaddr
                            addr_obj["netmask"] = netmask
                            addr_obj["broadcast"] = broadcast
                            addr_obj["label"] = iflabel
                            data["inet"].append(addr_obj)
                        elif type_ == "inet6":
                            if "inet6" not in data:
                                data["inet6"] = list()
                            addr_obj = dict()
                            addr_obj["address"] = ipaddr
                            addr_obj["prefixlen"] = netmask
                            addr_obj["scope"] = scope
                            data["inet6"].append(addr_obj)
                    else:
                        if "secondary" not in data:
                            data["secondary"] = list()
                        ip_, mask, brd, scp = await _parse_network(type_, value, cols)
                        data["secondary"].append(
                            {
                                "type": type_,
                                "address": ip_,
                                "netmask": mask,
                                "broadcast": brd,
                                "label": iflabel,
                            }
                        )
                        del ip_, mask, brd, scp
                elif type_.startswith("link"):
                    data["hwaddr"] = value
        if iface:
            ret[iface] = data
            del iface, data
    return ret


async def load_interfaces(hub):
    """
    Provide a dict of the connected interfaces and their ip addresses
    The addresses will be passed as a list for each interface
    """
    hub.log.debug("Loading interfaces")
    # Provides:
    #   ip_interfaces
    ipv4 = []
    ipv6 = []
    ip_path = shutil.which("ip")
    ifconfig_path = shutil.which("ifconfig")
    if ip_path:
        ret1 = await hub.exec.cmd.run(
            f"{ip_path} link show", stderr=asyncio.subprocess.STDOUT
        )
        ret2 = await hub.exec.cmd.run(
            f"{ip_path} addr show", stderr=asyncio.subprocess.STDOUT
        )
        interfaces = await _interfaces_ip(
            f"{ret1['stdout'].strip()}\n{ret2['stdout'].strip()}"
        )
    elif ifconfig_path:
        ret = await hub.exec.cmd.run(f"{ifconfig_path} -a")
        interfaces = await _interfaces_ifconfig(str(ret.stdout.strip()))
    else:
        hub.log.info(
            "Unable to find commands `ip` or `ifconfig` to detect network devices"
        )
        return

    interface: str
    device: Dict[str, Any]
    for interface, device in interfaces.items():
        if not interface:
            continue
        hw_addr = device.get("hwaddr")
        if hw_addr:
            hub.grains.GRAINS.hwaddr_interfaces[interface] = hw_addr
        inet4: List[str] = [ip.get("address") for ip in device.get("inet", [])]
        ipv4.extend(inet4)
        if inet4:
            hub.grains.GRAINS.ip4_interfaces[interface] = sorted(inet4)
        inet6: List[str] = [ip.get("address") for ip in device.get("inet6", [])]
        ipv6.extend(inet6)
        if inet6:
            hub.grains.GRAINS.ip6_interfaces[interface] = sorted(inet6)
        hub.grains.GRAINS.ip_interfaces[interface] = sorted(inet4) + sorted(inet6)

    hub.grains.GRAINS.ipv4 = sorted(ipv4)
    hub.grains.GRAINS.ipv6 = sorted(ipv6)
