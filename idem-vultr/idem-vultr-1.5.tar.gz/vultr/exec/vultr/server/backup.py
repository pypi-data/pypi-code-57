from typing import Any, Dict, Tuple

__func_alias__ = {
    "list_": "list",
}


async def disable(hub, ctx, subid: int) -> Tuple[bool, Dict[str, Any]]:
    """
    Disables automatic backups on a server. Once disabled, backups can only be enabled again by customer support.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.server.backup.disable
    """
    return await hub.exec.vultr.util.query(
        ctx, "server/backup_disable", method="POST", SUBID=subid
    )


async def enable(hub, ctx, subid: int) -> Tuple[bool, Dict[str, Any]]:
    """
    Enables automatic backups on a server.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.server.backup.enable
    """
    return await hub.exec.vultr.util.query(
        ctx, "server/backup_enable", method="POST", SUBID=subid
    )


async def restore(hub, ctx, subid: int, backup: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Restore the specified backup to the virtual machine.
    Any data already on the virtual machine will be lost.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.server.backup.restore
    """
    return await hub.exec.vultr.util.query(
        ctx, "server/restore_backup", method="POST", SUBID=subid, backup=backup
    )


async def get_schedule(hub, ctx, subid: int) -> Tuple[bool, Dict[str, Any]]:
    """
    Retrieves the backup schedule for a server. All time values are in UTC.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.server.backup.get_schedule
    """
    return await hub.exec.vultr.util.query(
        ctx, "server/backup_get_schedule", method="POST", SUBID=subid
    )


async def set_schedule(
    hub,
    ctx,
    subid: int,
    cron_type: str,
    hour: int = None,
    day_of_week: int = None,
    day_of_month: int = None,
) -> Tuple[bool, Dict[str, Any]]:
    """
    Retrieves the backup schedule for a server. All time values are in UTC.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.server.backup.get_schedule
    """
    kwargs = {}
    if hour is not None:
        kwargs["hour"] = hour
    if day_of_week is not None:
        kwargs["dow"] = day_of_week
    if day_of_month is not None:
        kwargs["dom"] = day_of_month
    return await hub.exec.vultr.util.query(
        ctx,
        "server/backup_get_schedule",
        method="POST",
        SUBID=subid,
        cron_type=cron_type,
        **kwargs,
    )
