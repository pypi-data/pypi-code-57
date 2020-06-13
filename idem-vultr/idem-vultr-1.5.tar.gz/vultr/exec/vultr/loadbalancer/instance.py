__func_alias__ = {
    "list_": "list",
}


async def attach(hub, ctx, subid: int, backend_node: int):
    """
    Attach an instance to a load balancer subscription.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.loadbalancer.instance.attach
    """
    return await hub.exec.vultr.util.query(
        ctx, "loadbalancer/generic_info", SUBID=subid, backendNode=backend_node
    )


async def detach(hub, ctx, subid: int, backend_node: int):
    """
    Detach an instance to a load balancer subscription.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.loadbalancer.instance.detach
    """
    return await hub.exec.vultr.util.query(
        ctx, "loadbalancer/generic_info", SUBID=subid, backendNode=backend_node
    )


async def list_(hub, ctx, subid: int):
    """
    List the instances attached to a load balancer subscription.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.loadbalancer.instance.list
    """
    return await hub.exec.vultr.util.query(
        ctx, "loadbalancer/generic_info", SUBID=subid
    )
