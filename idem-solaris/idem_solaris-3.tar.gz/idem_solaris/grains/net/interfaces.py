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
    pip = re.compile(r".*?(?:inet addr:|inet [^\d]*)(.*?)\s")
    pip6 = re.compile(".*?(?:inet6 addr: (.*?)/|inet6 )([0-9a-fA-F:]+)")
    pmask6 = re.compile(r".*?(?:inet6 addr: [0-9a-fA-F:]+/(\d+)|)")
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
            mip = pip.match(line)
            mip6 = pip6.match(line)
            mupdown = pupdown.search(line)
            if miface:
                iface = miface.group(1)
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
                    if addr_obj["address"] != "::":
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


async def _get_hwaddr_interfaces4(hub) -> Dict[str, str]:
    """
    Read netstat and look for mac addresses
    """
    result = {}
    netstat = shutil.which("netstat")
    if netstat:
        hwaddr = re.compile(
            "\w+\s+([\d|\.]+)\s+[\w|\.]+\s+\w*\s+((?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2}))$"
        )
        ret = await hub.exec.cmd.run([netstat, "-p", "-n", "-f", "inet"])
        for line in ret.stdout.splitlines():
            match = hwaddr.match(line.strip())
            if match:
                result[match.group(1)] = match.group(2)
    return result


async def _get_hwaddr_interfaces6(hub) -> Dict[str, str]:
    """
    Read netstat and look for mac addresses
    """
    result = {}
    netstat = shutil.which("netstat")
    if netstat:
        hwaddr = re.compile(
            "\w+\s+((?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2}))\s+\w+\s+\w+\s+([0-9a-fA-F|:]+)$"
        )
        ret = await hub.exec.cmd.run([netstat, "-p", "-n", "-f", "inet6"])
        for line in ret.stdout.splitlines():
            match = hwaddr.match(line.strip())
            if match:
                result[match.group(2)] = match.group(1)
    return result


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

    # Start collecting mac addresses
    hwaddrs = await _get_hwaddr_interfaces4(hub)
    hwaddrs.update(await _get_hwaddr_interfaces6(hub))

    ifconfig_path = shutil.which("ifconfig")
    if ifconfig_path:
        ret = await hub.exec.cmd.run([ifconfig_path, "-a"])
        interfaces = await _interfaces_ifconfig(str(ret.stdout.strip()))

        for interface, device in interfaces.items():
            if not interface:
                continue
            inet4: List[str] = [ip.get("address") for ip in device.get("inet", [])]
            ipv4.extend(inet4)
            if inet4:
                hub.grains.GRAINS.ip4_interfaces[interface] = sorted(inet4)
            inet6: List[str] = [ip.get("address") for ip in device.get("inet6", [])]
            ipv6.extend(inet6)
            if inet6:
                hub.grains.GRAINS.ip6_interfaces[interface] = sorted(inet6)
            hub.grains.GRAINS.ip_interfaces[interface] = sorted(inet4) + sorted(inet6)

            for addr in ipv4 + ipv6:
                hw_addr = hwaddrs.get(addr)
                if hw_addr:
                    hub.grains.GRAINS.hwaddr_interfaces[interface] = hw_addr
                    break
    hub.grains.GRAINS.ipv4 = sorted(ipv4)
    hub.grains.GRAINS.ipv6 = sorted(ipv6)
