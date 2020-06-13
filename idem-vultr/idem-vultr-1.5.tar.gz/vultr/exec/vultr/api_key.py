from typing import Any, Dict, Tuple

__virtualname__ = "apikey"
__func_alias__ = {
    "info": "get",
}


async def info(hub, ctx) -> Dict[str, Dict[str, Any]]:
    r"""
    Retrieve information about the current API key.

    CLI Example:

    .. code-block:: bash

        idem exec vultr.key.get
    """
    return await hub.exec.vultr.util.query(ctx, "auth/info")
