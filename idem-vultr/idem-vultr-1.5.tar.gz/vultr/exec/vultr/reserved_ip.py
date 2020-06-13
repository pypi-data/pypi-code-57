from typing import Any, Dict, Tuple, List

__virtualname__ = "ip"
__func_alias__ = {
    "destroy": "delete",
    "list_": "list",
}


async def attach(hub, ctx, subid: int, ip: str):
    """
    Attach a reserved IP to an existing subscription.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.reserved_ip.attach
    """
    return await hub.exec.vultr.util.query(
        ctx, "reservedip/attach", method="POST", ip_address=ip, attach_SUBID=subid
    )


async def convert(hub, ctx, subid: int, ip: str, **kwargs):
    """
    Convert an existing IP on a subscription to a reserved IP.
    Returns the SUBID of the newly created reserved IP.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.reserved_ip.attach
    """
    return await hub.exec.vultr.util.query(
        ctx, "reservedip/convert", method="POST", ip_address=ip, SUBID=subid, **kwargs
    )


async def create(hub, ctx, ip_type: str, **kwargs):
    """
    Create a new reserved IP.
    Reserved IPs can only be used within the same datacenter for which they were created.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.reserved_ip.create
    """
    return await hub.exec.vultr.util.query(
        ctx, "reservedip/create", method="POST", raw_ip_type=ip_type, **kwargs,
    )


async def destroy(hub, ctx, ip: str):
    """
    Remove a reserved IP from your account. After making this call, you will not be able to recover the IP address.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.reserved_ip.delete
    """
    return await hub.exec.vultr.util.query(
        ctx, "reservedip/destroy", method="POST", ip_address=ip
    )


async def detach(hub, ctx, subid: str, ip: str):
    """
    Detach a reserved IP from an existing subscription.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.reserved_ip.detach
    """
    return await hub.exec.vultr.util.query(
        ctx, "reservedip/list", method="POST", ip_address=ip, detach_SUBID=subid
    )


async def list_(hub, ctx):
    """
    List all the active reserved IPs on this account.
    The "subnet_size" field is the size of the network assigned to this subscription.
    This will typically be a /64 for IPv6, or a /32 for IPv4.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.reserved_ip.list
    """
    return await hub.exec.vultr.util.query(ctx, "reservedip/list", method="POST")
