from typing import Any, Dict, Tuple

__virtualname__ = "iso"
__func_alias__ = {
    "create_from_url": "create",
    "destroy": "delete",
    "list_": "list",
}


async def create_from_url(hub, ctx, url: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Create a new ISO image on the current account.
    The ISO image will be downloaded from a given URL.
    Download status can be checked with the v1/iso/list call.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.iso.create
    """
    return await hub.exec.vultr.util.query(
        ctx, "iso/create_from_url", method="POST", url=url
    )


async def destroy(hub, ctx, iso: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Destroy (delete) an ISO image. There is no going back from this call.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.iso.delete
    """
    return await hub.exec.vultr.util.query(ctx, "iso/delete", method="POST", iso=iso)


async def list_(hub, ctx, public: bool = False) -> Tuple[bool, Dict[str, Any]]:
    """
    List all ISOs currently available on this account.
    if `public` is true then list public ISOs offered in the Vultr ISO library.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.iso.list
    """
    if public:
        return await hub.exec.vultr.util.query(ctx, "iso/list_public")
    else:
        return await hub.exec.vultr.util.query(ctx, "iso/list")
