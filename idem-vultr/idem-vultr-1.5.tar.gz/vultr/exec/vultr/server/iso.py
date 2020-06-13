from typing import Any, Dict, Tuple

__func_alias__ = {"status": "get"}


async def attach(hub, ctx, subid: int, iso: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Attach an ISO and reboot the server.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.server.iso.attach
    """
    return await hub.exec.vultr.util.query(
        ctx, "server/iso_attach", method="POST", SUBID=subid, iso=iso
    )


async def detach(hub, ctx, subid: int) -> Tuple[bool, Dict[str, Any]]:
    """
    Detach the currently mounted ISO and reboot the server.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.server.iso.detach
    """
    return await hub.exec.vultr.util.query(
        ctx, "server/iso_detach", method="POST", SUBID=subid
    )


async def status(hub, ctx, subid: int) -> Tuple[bool, Dict[str, Any]]:
    """
    Retrieve the current ISO state for a given subscription.
    The returned state may be one of: ready | isomounting | isomounted.
    ISOID will only be set when the mounted ISO exists in your library ( see /v1/iso/list ).
    Otherwise, it will read "0".

    CLI Example:

    .. code-block:: bash
        idem exec vultr.server.iso.get
    """
    return await hub.exec.vultr.util.query(ctx, "server/iso_status", SUBID=subid)
