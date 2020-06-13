from typing import Any, Dict, Tuple

__func_alias__ = {
    "destroy": "delete",
    "list_": "list",
}


async def create(
    hub, ctx, subid: int, reboot: bool = True
) -> Tuple[bool, Dict[str, Any]]:
    """
    Create a new virtual machine.
    You will start being billed for this immediately.
    The response only contains the SUBID for the new machine.

    To determine that a server is ready for use, you may poll /v1/server/list?SUBID=<SUBID> and check that the "status" field is set to "active", then test your OS login with SSH (Linux) or RDP (Windows).

    In order to create a server using a snapshot, use OSID 164 and specify a snapshot.
    Similarly, to create a server using an ISO use OSID 159 and specify an iso.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.server.ipv4.create
    """
    return await hub.exec.vultr.util.query(
        ctx,
        "server/create_ipv4",
        method="POST",
        SUBID=subid,
        reboot="yes" if reboot else "no",
    )


async def destroy(hub, ctx, subid: int, ip: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Removes a secondary IPv4 address from a server.
    Your server will be hard-restarted.
    We suggest halting the machine gracefully before removing IPs.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.server.ipv4.delete
    """
    return await hub.exec.vultr.util.query(
        ctx, "server/destroy_ipv4", method="POST", SUBID=subid, ip=ip
    )


async def list_(hub, ctx, subid: int, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    """
    List the IPv4 information of a virtual machine.
    IP information is only available for virtual machines in the "active" state.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.server.ipv4.list
    """
    return await hub.exec.vultr.util.query(
        ctx, "server/list_ipv4", SUBID=subid, **kwargs
    )


async def reverse(
    hub, ctx, subid: int, ip: str, entry: str = None
) -> Tuple[bool, Dict[str, Any]]:
    """
    Set a reverse DNS entry for an IPv4 address of a virtual machine to the original setting.
    Upon success, DNS changes may take 6-12 hours to become active.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.server.ipv4.reverse
    """
    if entry is None:
        return await hub.exec.vultr.util.query(
            ctx, "server/reverse_default_ipv4", method="POST", SUBID=subid, ip=ip
        )
    else:
        return await hub.exec.vultr.util.query(
            ctx,
            "server/reverse_set_ipv4",
            method="POST",
            SUBID=subid,
            ip=ip,
            entry=entry,
        )
