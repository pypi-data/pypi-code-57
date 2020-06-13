from typing import Any, Dict, Tuple

__virtualname__ = "os"
__func_alias__ = {
    "list_": "list",
}


async def change(hub, ctx, subid: int, os: str) -> Dict[str, Dict[str, Any]]:
    r"""
    Changes the bare metal server to a different operating system. All data will be permanently lost.

    CLI Example:

    .. code-block:: bash

        idem exec vultr.baremetal.os_change
    """
    return await hub.exec.vultr.util.query(
        ctx, "baremetal/os_change", method="POST", SUBID=subid, os=os
    )


async def list_(hub, ctx, subid: int) -> Dict[str, Dict[str, Any]]:
    r"""
    Retrieves a list of operating systems to which a bare metal server can be changed.
    Always check against this list before trying to switch operating systems because it is not possible to switch between every operating system combination.

    The "surcharge" field is deprecated and will always be set to zero.

    CLI Example:

    .. code-block:: bash

        idem exec vultr.baremetal.os_change_list
    """
    return await hub.exec.vultr.util.query(
        ctx, "baremetal/os_change_list", method="POST", SUBID=subid
    )
