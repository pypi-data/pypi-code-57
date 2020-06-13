from typing import Any, Dict, Tuple

__func_alias__ = {
    "list_": "list",
    "get_user_data": "get",
    "set_user_data": "set",
}


async def get_user_data(hub, ctx, subid: int) -> Dict[str, Dict[str, Any]]:
    r"""
    Retrieves the (base64 encoded) user-data for this subscription.

    CLI Example:

    .. code-block:: bash

        idem exec vultr.baremetal.list
    """
    return await hub.exec.vultr.util.query(ctx, "baremetal/get_user_data", SUBID=subid)


async def set_user_data(
    hub, ctx, subid: int, userdata: str
) -> Dict[str, Dict[str, Any]]:
    r"""
    Sets the user-data for this subscription. User-data is a generic data store, which some provisioning tools and cloud operating systems use as a configuration file. It is generally consumed only once after an instance has been launched, but individual needs may vary.

    CLI Example:

    .. code-block:: bash

        idem exec vultr.baremetal.set_user_data
    """
    return await hub.exec.vultr.util.query(
        ctx, "baremetal/set_user_data", method="POST", SUBID=subid, userdata=userdata
    )
