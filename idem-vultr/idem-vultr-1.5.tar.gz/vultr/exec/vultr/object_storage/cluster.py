from typing import Any, Dict, Tuple

__func_alias__ = {
    "list_": "list",
}


async def list_(hub, ctx) -> Tuple[bool, Dict[str, Any]]:
    """
    List all domains associated with the current account.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.object.list_cluster
    """
    return await hub.exec.vultr.util.query(ctx, "objectstorage/list_cluster")
