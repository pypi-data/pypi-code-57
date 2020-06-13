from typing import Any, Dict, Tuple

__func_alias__ = {
    "destroy": "delete",
    "list_": "list",
}


async def create(hub, ctx, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    """
    Create a domain name in DNS.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.network.create
    """
    return await hub.exec.vultr.util.query(
        ctx, "network/create", method="POST", **kwargs
    )


async def destroy(hub, ctx, network: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Destroy (delete) a private network.
    Before destroying, a network must be disabled from all instances.
    See /v1/server/private_network_disable.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.network.delete
    """
    return await hub.exec.vultr.util.query(
        ctx, "network/destroy", method="POST", network=network
    )


async def list_(hub, ctx) -> Tuple[bool, Dict[str, Any]]:
    """
    List all domains associated with the current account.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.network.list
    """
    return await hub.exec.vultr.util.query(ctx, "network/list")
