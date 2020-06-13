import enum
import ipaddress
from typing import Any, Dict, Tuple

__func_alias__ = {
    "list_": "list",
}


class IPType(enum.IntEnum):
    v4 = 4
    v6 = 6


class Protocol(enum.Enum):
    icmp = "icmp"
    tcp = "tcp"
    udp = "udp"
    gre = "gre"


async def create(
    hub,
    ctx,
    firewall_group: str,
    ip_type: int,
    protocol: str,
    subnet: str,
    subnet_size: int,
    port: str = None,
    notes: str = "",
    source: str = "",
) -> Tuple[bool, Dict[str, Any]]:
    """
    Create a domain name in DNS.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.firewall.group.create
    """
    kwargs = {}
    if port is not None:
        kwargs["port"] = port
    if notes is not None:
        kwargs["notes"] = notes
    if source is not None:
        kwargs["source"] = source

    return await hub.exec.vultr.util.query(
        ctx,
        "firewall/rule_create",
        method="POST",
        firewall_group=firewall_group,
        raw_ip_type=IPType(ip_type).name,
        protocol=Protocol(protocol).name,
        subnet=str(
            ipaddress.IPv6Address(subnet)
            if protocol == 6
            else ipaddress.IPv4Address(subnet)
        ),
        subnet_size=subnet_size,
        raw_direction="in",  # "in" is the only option for directino
        **kwargs,
    )


async def delete(
    hub, ctx, rule_number: int, firewall_group: str
) -> Tuple[bool, Dict[str, Any]]:
    """
    Delete a domain name and all associated records.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.firewall.group.delete
    """
    return await hub.exec.vultr.util.query(
        ctx,
        "firewall/rule_delete",
        method="POST",
        firewall_group=firewall_group,
        rulenumber=rule_number,
    )


async def list_(
    hub, ctx, firewall_group: int = None, ip_type: str = None
) -> Tuple[bool, Dict[str, Any]]:
    """
    List all domains associated with the current account.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.firewall.group.list
    """
    if firewall_group is not None:
        firewall_groups = [firewall_group]
    else:
        firewall_groups = [
            v.get("FIREWALLGROUPID")
            for v in (await hub.exec.vultr.firewall.group.list(ctx))[1].values()
            if v.get("rule_count")
        ]
    if ip_type is not None:
        ip_types = [ip_type]
    else:
        ip_types = ["v4", "v6"]

    result = {}
    status = True
    for fg in firewall_groups:
        for ipt in ip_types:
            status, ret = await hub.exec.vultr.util.query(
                ctx,
                "firewall/rule_list",
                raw_FIREWALLGROUPID=fg,
                raw_direction="in",
                raw_ip_type=ipt,
            )
            status &= status
            result.update(ret)

    return status, result
