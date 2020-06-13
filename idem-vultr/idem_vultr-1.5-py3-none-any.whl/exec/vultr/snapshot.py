from typing import Any, Dict, Tuple, List

__func_alias__ = {
    "destroy": "delete",
    "list_": "list",
}


async def create(
    hub, ctx, subid: int, url: str = None, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    """
    Create a snapshot from an existing virtual machine.
    The virtual machine does not need to be stopped.
    
    If a url is provided then create a new snapshot on the current account.
    The snapshot will be downloaded from a given URL.
    Download status can be checked with the v1/snapshot/list call.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.snapshot.create
    """
    if url is None:
        return await hub.exec.vultr.util.query(
            ctx, "snapshot/create_from_url", method="POST", SUBID=subid, **kwargs
        )
    else:
        return await hub.exec.vultr.util.query(
            ctx, "snapshot/create", method="POST", SUBID=subid, url=url
        )


async def destroy(hub, ctx, snapshot: str) -> Tuple[bool, Dict[str, Any]]:
    """

    CLI Example:

    .. code-block:: bash
        idem exec vultr.snapshot.delete
    """
    return await hub.exec.vultr.util.query(
        ctx, "snapshot/destroy", method="POST", snapshot=snapshot
    )


async def list_(hub, ctx, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    """

    CLI Example:

    .. code-block:: bash
        idem exec vultr.snapshot.list
    """
    return await hub.exec.vultr.util.query(ctx, "snapshot/list", **kwargs)


async def restore(hub, ctx, subid: int, snapshot: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Restore the specified backup to the virtual machine.
    Any data already on the virtual machine will be lost.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.snapshot.restore
    """
    return await hub.exec.vultr.util.query(
        ctx, "server/restore_snapshot", method="POST", SUBID=subid, snapshot=snapshot,
    )
