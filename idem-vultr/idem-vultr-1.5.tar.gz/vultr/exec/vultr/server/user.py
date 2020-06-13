from typing import Any, Dict, Tuple

__func_alias__ = {
    "destroy": "delete",
    "list_": "list",
    "get_user_data": "get",
    "set_user_data": "create",
}


async def get_user_data(hub, ctx, subid: int) -> Tuple[bool, Dict[str, Any]]:
    """
    Retrieves the (base64 encoded) user-data for this subscription.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.server.user.get
    """
    return await hub.exec.vultr.util.query(ctx, "server/get_user_data", SUBID=subid)


async def set_user_data(hub, ctx, userdata: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Sets the user-data for this subscription.
    User-data is a generic data store, which some provisioning tools and cloud operating systems use as a configuration file.
    It is generally consumed only once after an instance has been launched, but individual needs may vary.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.server.user.create
    """
    return await hub.exec.vultr.util.query(
        ctx, "server/set_user_data", method="POST", userdata=userdata
    )
