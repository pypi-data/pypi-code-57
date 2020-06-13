from typing import Any, Dict, Tuple

__func_alias__ = {
    "list_": "list",
    "info": "get",
}


async def change(hub, ctx, subid: int, app: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Changes the virtual machine to a different application. All data will be permanently lost.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.server.app.change
    """
    return await hub.exec.vultr.util.query(
        ctx, "server/app_change", method="POST", SUBID=subid, app=app
    )


async def list_(hub, ctx, subid: int) -> Tuple[bool, Dict[str, Any]]:
    """
    Retrieves a list of applications to which a virtual machine can be changed.
    Always check against this list before trying to switch applications because it is not possible to switch between every application combination.

    The "surcharge" field is deprecated and will always be set to zero.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.server.app.list
    """
    return await hub.exec.vultr.util.query(ctx, "server/app_change_list", SUBID=subid)


async def info(hub, ctx, subid: int) -> Tuple[bool, Dict[str, Any]]:
    """
    Retrieves a list of applications to which a virtual machine can be changed.
    Always check against this list before trying to switch applications because it is not possible to switch between every application combination.

    The "surcharge" field is deprecated and will always be set to zero.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.server.app.get
    """
    return await hub.exec.vultr.util.query(ctx, "server/get_app_info", SUBID=subid)
