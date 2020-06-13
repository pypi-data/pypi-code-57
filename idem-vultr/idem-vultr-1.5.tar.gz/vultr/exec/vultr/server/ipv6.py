from typing import Any, Dict, Tuple

__func_alias__ = {
    "list_": "list",
}


async def enable(hub, ctx, subid: int) -> Tuple[bool, Dict[str, Any]]:
    """
    Enables IPv6 networking on a server by assigning an IPv6 subnet to it.
    The server will be automatically rebooted to complete the request.
    No action occurs if IPv6 networking was already enabled.
    It is possible to check whether or not IPv6 networking has been enabled with v1/server/list_ipv6.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.server.ipv6.enable
    """
    return await hub.exec.vultr.util.query(
        ctx, "server/ipv6_enable", method="POST", SUBID=subid,
    )


async def list_(
    hub, ctx, subid: int, reverse: bool = False
) -> Tuple[bool, Dict[str, Any]]:
    """
    List the IPv6 information of a virtual machine.
    IP information is only available for virtual machines in the "active" state.
    If the virtual machine does not have IPv6 enabled, then an empty array is returned.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.server.vm.list
    """
    if reverse:
        return await hub.exec.vultr.util.query(
            ctx, "server/reverse_list_ipv6", SUBID=subid
        )
    else:
        return await hub.exec.vultr.util.query(ctx, "server/list_ipv6", SUBID=subid)


async def reverse_delete(hub, ctx, subid: int, ip: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Set a reverse DNS entry for an IPv4 address of a virtual machine to the original setting.
    Upon success, DNS changes may take 6-12 hours to become active.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.server.ipv6.delete
    """
    return await hub.exec.vultr.util.query(
        ctx, "server/reverse_delete_ipv6", method="POST", SUBID=subid, ip=ip
    )


async def reverse(
    hub, ctx, subid: int, ip: str, entry: str
) -> Tuple[bool, Dict[str, Any]]:
    """
    Set a reverse DNS entry for an IPv6 address of a virtual machine.
    Upon success, DNS changes may take 6-12 hours to become active.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.server.ipv4.reverse
    """
    return await hub.exec.vultr.util.query(
        ctx, "server/reverse_set_ipv6", method="POST", SUBID=subid, ip=ip, entry=entry
    )
