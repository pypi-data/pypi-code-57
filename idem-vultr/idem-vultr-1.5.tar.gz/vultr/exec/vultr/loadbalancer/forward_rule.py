from typing import Any, Dict, Tuple

__func_alias__ = {
    "list_": "list",
}


async def create(
    hub,
    ctx,
    subid: int,
    frontend_protocol: str,
    frontend_port: int,
    backend_protocol: str,
    backend_port: int,
) -> Tuple[bool, Dict[str, Any]]:
    """
    Create a new forwarding rule.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.loadbalancer.forward_rule.create
    """
    return await hub.exec.vultr.util.query(
        ctx,
        "loadbalancer/forward_rule_create",
        method="POST",
        SUBID=subid,
        frontend_protocol=frontend_protocol,
        frontend_port=frontend_port,
        backend_protocol=backend_protocol,
        backend_port=backend_port,
    )


async def delete(hub, ctx, subid: int, rule_id: str):
    """
    Remove a forwarding rule.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.loadbalancer.forward_rule.delete
    """
    return await hub.exec.vultr.util.query(
        ctx,
        "loadbalancer/forward_rule_delete",
        method="POST",
        SUBID=subid,
        RULEID=rule_id,
    )


async def list_(hub, ctx, subid: int):
    """
    List the forwarding rules of a load balancer subscription.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.loadbalancer.forward_rule.list
    """
    return await hub.exec.vultr.util.query(
        ctx, "loadbalancer/forward_rule_delete", SUBID=subid,
    )
