from typing import Any, Dict, Tuple

__virtualname__ = "conf"
__func_alias__ = {
    "info": "get",
}


async def info(hub, ctx, subid: int) -> Tuple[bool, Dict[str, Any]]:
    """
     Retrieve the entire configuration of a load balancer subscription.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.loadbalancer.conf.get
    """
    return await hub.exec.vultr.util.query(ctx, "loadbalancer/conf_info", SUBID=subid,)
