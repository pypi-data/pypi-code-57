__virtualname__ = "health"
__func_alias__ = {
    "info": "get",
}


async def info(hub, ctx, subid: int):
    """
    Retrieve the health checking configuration of a load balancer subscription.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.loadbalancer.generic.get
    """
    return await hub.exec.vultr.util.query(
        ctx, "loadbalancer/health_check_info", SUBID=subid,
    )


async def update(hub, ctx, subid: int, **kwargs):
    """
    Update the health checking configuration of a load balancer subscription.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.loadbalancer.generic.get
    """
    return await hub.exec.vultr.util.query(
        ctx, "loadbalancer/health_check_update", SUBID=subid, **kwargs
    )
