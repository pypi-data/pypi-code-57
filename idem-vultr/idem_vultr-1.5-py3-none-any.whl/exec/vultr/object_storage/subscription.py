import asyncio
from typing import Any, Dict, Tuple

__func_alias__ = {
    "destroy": "delete",
    "label_set": "label",
    "list_": "list",
}


async def create(hub, ctx, cluster: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    """
    Create an object storage subscription.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.object_storage.subscription.create
    """
    result, status = await hub.exec.vultr.util.query(
        ctx, "objectstorage/create", method="POST", cluster=cluster, **kwargs,
    )
    if result:
        subid = status["SUBID"]
        r2, s2 = await hub.exec.vultr.object_storage.subscription.list(
            ctx, raw_SUBID=subid
        )
        # wait for "status" to be "active"
        time_start = 0
        while s2["status"] != "active":
            time_start += hub.OPT.idem.vultr_check_interval
            await asyncio.sleep(hub.OPT.idem.vultr_check_interval)
            r2, s2 = await hub.exec.vultr.object_storage.subscription.list(
                ctx, raw_SUBID=subid
            )
            if (
                hub.OPT.idem.vultr_timeout is not None
                and time_start >= hub.OPT.idem.vultr_timeout
            ):
                hub.log.error(
                    f"Timeout reached while waiting for object storage to become active: {subid}"
                )
                break

    return result, status


async def destroy(hub, ctx, subid: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Destroy (delete) a private network.
    Before destroying, a network must be disabled from all instances.
    See /v1/server/private_network_disable.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.object_storage.subscription.delete
    """
    return await hub.exec.vultr.util.query(
        ctx, "objectstorage/destroy", method="POST", SUBID=subid
    )


async def label_set(hub, ctx, subid: int, label: str) -> Tuple[bool, Dict[str, Any]]:
    """
    List all domains associated with the current account.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.object_storage.subscription.list
    """
    return await hub.exec.vultr.util.query(
        ctx, "objectstorage/label_set", method="POST", raw_label=label, SUBID=subid
    )


async def list_(hub, ctx, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    """
    List all domains associated with the current account.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.object_storage.subscription.list
    """
    return await hub.exec.vultr.util.query(ctx, "objectstorage/list", **kwargs)
