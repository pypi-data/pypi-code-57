__func_alias__ = {
    "info": "get",
}


async def info(hub, ctx, subid: int):
    """
    Retrieve the generic configuration of a load balancer subscription.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.loadbalancer.generic.get
    """
    return await hub.exec.vultr.util.query(
        ctx, "loadbalancer/generic_info", SUBID=subid,
    )


async def update(hub, ctx, subid: int, **kwargs):
    """
    Retrieve the generic configuration of a load balancer subscription.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.loadbalancer.generic.update
    """
    return await hub.exec.vultr.util.query(
        ctx, "loadbalancer/generic_info", method="POST", SUBID=subid, **kwargs
    )
