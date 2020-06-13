import asyncio
from typing import Any, Dict, Tuple

__func_alias__ = {
    "destroy": "delete",
    "info": "get",
    "label_set": "label",
    "list_": "list",
}


async def create(hub, ctx, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    """
    Create a load balancer subscription.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.loadbalancer.subscription.create
    """
    result, status = await hub.exec.vultr.util.query(
        ctx, "loadbalancer/create", method="POST", **kwargs
    )

    if result:
        subid = status["SUBID"]
        r2, s2 = await hub.exec.vultr.loadbalancer.subscription.list(
            ctx, raw_SUBID=subid
        )
        # wait for "status" to be "active"
        time_start = 0
        while s2["status"] != "active":
            time_start += hub.OPT.idem.vultr_check_interval
            await asyncio.sleep(hub.OPT.idem.vultr_check_interval)
            r2, s2 = await hub.exec.vultr.loadbalancer.subscription.list(
                ctx, raw_SUBID=subid
            )
            if (
                hub.OPT.idem.vultr_timeout is not None
                and time_start >= hub.OPT.idem.vultr_timeout
            ):
                hub.log.error(
                    f"Timeout reached while waiting for load balancer to become active: {subid}"
                )
                break

    return result, status


async def destroy(hub, ctx, subid: int) -> Tuple[bool, Dict[str, Any]]:
    """
    Destroy a load balancer subscription.
    All data will be permanently lost.
    Web traffic passing through the load balancer will be abruptly terminated.
    There is no going back from this call.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.loadbalancer.subscription.delete
    """
    return await hub.exec.vultr.util.query(
        ctx, "loadbalancer/destroy", method="POST", SUBID=subid,
    )


async def label_set(hub, ctx, subid: int, label: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Set the label of a load balancer subscription.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.loadbalancer.subscription.label
    """
    return await hub.exec.vultr.util.query(
        ctx, "loadbalancer/label_set", method="POST", SUBID=subid, raw_label=label
    )


async def list_(hub, ctx, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    """

    CLI Example:

    .. code-block:: bash
        idem exec vultr.loadbalancer.subscription.list
    """
    return await hub.exec.vultr.util.query(ctx, "loadbalancer/list", **kwargs)
