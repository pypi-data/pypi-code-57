from typing import Any, Dict, Tuple

__func_alias__ = {
    "list_": "list",
    "info": "get",
}


async def change(hub, ctx, subid: int, app: str) -> Dict[str, Dict[str, Any]]:
    r"""
    Reinstalls the bare metal server to a different Vultr one-click application. All data will be permanently lost.

    CLI Example:

    .. code-block:: bash

        idem exec vultr.baremetal.app_change
    """
    return await hub.exec.vultr.util.query(
        ctx, "baremetal/app_change", method="POST", SUBID=subid, app=app
    )


async def list_(hub, ctx, subid: int) -> Dict[str, Dict[str, Any]]:
    r"""
    Retrieves a list of Vultr one-click applications to which a bare metal server can be changed.
    Always check against this list before trying to switch applications because it is not possible to switch between every application combination.
    The "surcharge" field is deprecated and will always be set to zero.

    CLI Example:

    .. code-block:: bash

        idem exec vultr.baremetal.app_change_list
    """
    return await hub.exec.vultr.util.query(
        ctx, "baremetal/app_change_list", SUBID=subid
    )


async def info(hub, ctx, subid: int) -> Dict[str, Dict[str, Any]]:
    r"""
    Retrieves the application information for a bare metal server.

    CLI Example:

    .. code-block:: bash

        idem exec vultr.baremetal.get_app_info
    """
    return await hub.exec.vultr.util.query(ctx, "baremetal/get_app_info", SUBID=subid)
