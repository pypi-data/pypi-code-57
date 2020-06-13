__func_alias__ = {
    "add": "create",
    "info": "get",
    "remove": "delete",
}


async def add(
    hub, ctx, subid: str, ssl_private_key: str, ssl_certificate: str, **kwargs
):
    """
    Add a SSL certificate to a load balancer.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.loadbalancer.ssl.create
    """
    return await hub.exec.vultr.util.query(
        ctx,
        "loadbalancer/generic_info",
        method="POST",
        SUBID=subid,
        ssl_private_key=ssl_private_key,
        ssl_certificate=ssl_certificate,
        **kwargs,
    )


async def info(hub, ctx, subid: int):
    """
    Retrieve whether or not your load balancer subscription has an SSL cert attached.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.loadbalancer.ssl.get
    """
    return await hub.exec.vultr.util.query(
        ctx, "loadbalancer/generic_info", SUBID=subid
    )


async def remove(hub, ctx, subid: int):
    """
    Remove a SSL certificate to a load balancer.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.loadbalancer.ssl.delete
    """
    return await hub.exec.vultr.util.query(
        ctx, "loadbalancer/generic_info", SUBID=subid
    )
