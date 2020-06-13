from typing import Any, Dict, Tuple

__func_alias__ = {
    "list_": "list",
}


async def list_(hub, ctx, subid: int) -> Dict[str, Dict[str, Any]]:
    r"""
    List the IPv4 information of a bare metal server.
    IP information is only available for bare metal servers in the "active" state.

    CLI Example:

    .. code-block:: bash

        idem exec vultr.baremetal.list_ipv4
    """
    return await hub.exec.vultr.util.query(ctx, "baremetal/list_ipv4", SUBID=subid)
