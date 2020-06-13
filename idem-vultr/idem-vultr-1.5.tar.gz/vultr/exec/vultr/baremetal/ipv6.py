from typing import Any, Dict, Tuple

__func_alias__ = {
    "list_": "list",
}


async def enable(hub, ctx, subid: int) -> Dict[str, Dict[str, Any]]:
    r"""
    Enables IPv6 networking on a bare metal server by assigning an IPv6 subnet to it.
    The server will not be rebooted when the subnet is assigned. It is possible to check whether or not IPv6 networking has been enabled with v1/baremetal/list_ipv6.

    CLI Example:

    .. code-block:: bash

        idem exec vultr.baremetal.ipv6_enable
    """
    return await hub.exec.vultr.util.query(
        ctx, "baremetal/ipv6_enable", method="POST", SUBID=subid
    )


async def list_(hub, ctx, subid: int) -> Dict[str, Dict[str, Any]]:
    r"""
    List the IPv6 information of a bare metal server.
    IP information is only available for bare metal servers in the "active" state.
    If the bare metal server does not have IPv6 enabled, then an empty array is returned.

    CLI Example:

    .. code-block:: bash

        idem exec vultr.baremetal.list
    """
    return await hub.exec.vultr.util.query(ctx, "baremetal/list_ipv6", SUBID=subid)
