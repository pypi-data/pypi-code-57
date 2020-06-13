from typing import Any, Dict, Tuple


__func_alias__ = {
    "list_": "list",
}


async def list_(hub, ctx) -> Dict[str, Dict[str, Any]]:
    r"""
    Retrieve a list of available applications. These refer to applications that can be launched when creating a Vultr VPS.
    The "surcharge" field is deprecated and will always be set to zero.

    CLI Example:

    .. code-block:: bash

        idem exec vultr.bak.list
    """
    return await hub.exec.vultr.util.query(ctx, "backup/list")
