from typing import Any, Dict, Tuple

__virtualname__ = "app"
__func_alias__ = {
    "list_": "list",
}


async def list_(hub, ctx) -> Dict[str, Dict[str, Any]]:
    r"""
    List all backups on the current account.

    CLI Example:

    .. code-block:: bash

        idem exec vultr.app.list
    """
    return await hub.exec.vultr.util.query(ctx, "app/list")
