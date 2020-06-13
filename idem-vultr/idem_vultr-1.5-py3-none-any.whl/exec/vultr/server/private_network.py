from typing import Any, Dict, Tuple

__func_alias__ = {
    "list_": "list",
}


async def disable(hub, ctx, subid: int, network: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Removes a private network from a server.
    The server will be automatically rebooted to complete the request.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.server.private_networks.disable
    """
    return await hub.exec.vultr.util.query(
        ctx, "server/private_networks", SUBID=subid, network=network
    )


async def enable(hub, ctx, subid: int, network: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Enables private networking on a server.
    The server will be automatically rebooted to complete the request.
    No action occurs if private networking was already enabled.
    It is possible to check whether or not private networking has been enabled with v1/server/list_ipv4.

    If you have multiple private networks in a location, you will need to specify the network of the network that you want to attach.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.server.private_networks.enable
    """
    return await hub.exec.vultr.util.query(
        ctx, "server/private_networks", SUBID=subid, network=network
    )


async def list_(hub, ctx, subid: int) -> Tuple[bool, Dict[str, Any]]:
    """
    List private networks attached to a particular server.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.server.private_networks.list
    """
    return await hub.exec.vultr.util.query(ctx, "server/private_networks", SUBID=subid)
