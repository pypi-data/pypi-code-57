from typing import Any, Dict, Tuple

__virtualname__ = "os"
__func_alias__ = {
    "list_": "list",
}


async def change(hub, ctx, subid: int, os: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Changes the virtual machine to a different operating system. All data will be permanently lost.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.server.os.change
    """
    return await hub.exec.vultr.util.query(
        ctx, "server/os_change", method="POST", SUBID=subid, os=os
    )


async def list_(hub, ctx, subid: int) -> Tuple[bool, Dict[str, Any]]:
    """
    Retrieves a list of operating systems to which a virtual machine can be changed.
    Always check against this list before trying to switch operating systems because it is not possible to switch between every operating system combination.

    The "surcharge" field is deprecated and will always be set to zero.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.server.os.list
    """
    return await hub.exec.vultr.util.query(ctx, "server/os_change_list", SUBID=subid)
