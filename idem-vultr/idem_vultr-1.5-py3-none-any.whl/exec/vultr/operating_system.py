from typing import Any, Dict, Tuple

__virtualname__ = "os"

__func_alias__ = {
    "list_": "list",
}


async def list_(hub, ctx) -> Tuple[bool, Dict[str, Any]]:
    """
    Retrieve a list of available operating systems.
    If the "windows" flag is true, a Windows license will be included with the instance, which will increase the cost.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.os.list
    """
    return await hub.exec.vultr.util.query(ctx, "os/list")
