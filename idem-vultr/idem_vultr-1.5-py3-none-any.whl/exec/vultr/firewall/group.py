from typing import Any, Dict, Tuple

__func_alias__ = {
    "list_": "list",
    "set_description": "description",
}


async def create(hub, ctx, description: str = None) -> Tuple[bool, Dict[str, Any]]:
    """
    Create a domain name in DNS.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.firewall.group.create
    """
    kwargs = {}
    if description is not None:
        kwargs["description"] = description
    return await hub.exec.vultr.util.query(
        ctx, "firewall/group_create", method="POST", **kwargs
    )


async def delete(hub, ctx, firewall_group: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Delete a domain name and all associated records.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.firewall.group.delete
    """
    return await hub.exec.vultr.util.query(
        ctx, "firewall/group_delete", method="POST", firewall_group=firewall_group
    )


async def list_(hub, ctx) -> Tuple[bool, Dict[str, Any]]:
    """
    List all domains associated with the current account.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.firewall.group.list
    """
    return await hub.exec.vultr.util.query(ctx, "firewall/group_list", method="GET")


async def set_description(
    hub, ctx, firewall_group: str, description: str
) -> Tuple[bool, Dict[str, Any]]:
    """
    List all domains associated with the current account.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.firewall.group.description
    """
    return await hub.exec.vultr.util.query(
        ctx,
        "firewall/group_set_description",
        firewall_group=firewall_group,
        description=description,
    )
