from typing import Any, Dict, Tuple

__virtualname__ = "block"
__func_alias__ = {
    "label_set": "label",
    "list_": "list",
}


async def attach(
    hub, ctx, subid: int, attach_to_subid: int, live: bool = False
) -> Dict[str, Dict[str, Any]]:
    r"""
    Attach a block storage subscription to a VPS subscription.
    The instance will be restarted.
    The block storage volume must not be attached to any other VPS subscriptions for this to work.

    CLI Example:

    .. code-block:: bash

        idem exec vultr.block.attach
    """
    return await hub.exec.vultr.util.query(
        ctx,
        "block/attach",
        method="POST",
        SUBID=subid,
        attach_to_SUBID=attach_to_subid,
        live="yes" if live else "no",
    )


async def create(hub, ctx, size_gb: int, label: str) -> Dict[str, Dict[str, Any]]:
    r"""
    Create a block storage subscription.

    CLI Example:

    .. code-block:: bash

        idem exec vultr.block.create
    """
    return await hub.exec.vultr.util.query(
        ctx, "block/create", method="POST", size_gb=size_gb, raw_label=label
    )


async def delete(hub, ctx, subid: int) -> Dict[str, Dict[str, Any]]:
    r"""
    Delete a block storage subscription.
    All data will be permanently lost.
    There is no going back from this call.

    CLI Example:

    .. code-block:: bash

        idem exec vultr.block.delete
    """
    return await hub.exec.vultr.util.query(
        ctx, "block/delete", method="POST", SUBID=subid
    )


async def detach(hub, ctx, subid: int, live: bool = False) -> Dict[str, Dict[str, Any]]:
    r"""
    Detach a block storage subscription from the currently attached instance.
    The instance will be restarted.

    We do not recommend using live detaches unless you are certain that the volume has been unmounted from your operating system.
    Detaching a mounted volume may result in data loss/corruption.

    CLI Example:

    .. code-block:: bash

        idem exec vultr.block.detach
    """
    return await hub.exec.vultr.util.query(
        ctx, "block/detach", method="POST", SUBID=subid, live="yes" if live else "no"
    )


async def label_set(hub, ctx, subid: int, label: str) -> Dict[str, Dict[str, Any]]:
    r"""
    Detach a block storage subscription from the currently attached instance.
    The instance will be restarted.

    We do not recommend using live detaches unless you are certain that the volume has been unmounted from your operating system.
    Detaching a mounted volume may result in data loss/corruption.

    CLI Example:

    .. code-block:: bash

        idem exec vultr.block.label
    """
    return await hub.exec.vultr.util.query(
        ctx, "block/label", method="POST", SUBID=subid, raw_label=label
    )


async def list_(hub, ctx, subid: int) -> Dict[str, Dict[str, Any]]:
    r"""

    CLI Example:

    .. code-block:: bash

        idem exec vultr.block.list
    """
    return await hub.exec.vultr.util.query(ctx, "block/list", SUBID=subid)


async def resize(hub, ctx, subid: int, size_gb: int) -> Dict[str, Dict[str, Any]]:
    r"""
    Resize the block storage volume to a new size.
    WARNING: When shrinking the volume, you must manually shrink the filesystem and partitions beforehand, or you will lose data.

    CLI Example:

    .. code-block:: bash

        idem exec vultr.block.list
    """
    return await hub.exec.vultr.util.query(
        ctx, "block/resize", method="POST", SUBID=subid, size_gb=size_gb
    )
