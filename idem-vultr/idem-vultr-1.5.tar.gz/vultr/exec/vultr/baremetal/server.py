import asyncio
from typing import Any, Dict, Tuple

__func_alias__ = {
    "destroy": "delete",
    "label_set": "label",
    "list_": "list",
    "tag_set": "tag",
}


async def bandwidth(hub, ctx, subid: int) -> Tuple[bool, Dict[str, Dict[str, Any]]]:
    r"""
    Get the bandwidth used by a bare metal server.

    CLI Example:

    .. code-block:: bash

        idem exec vultr.baremetal.bandwidth
    """
    return await hub.exec.vultr.util.query(ctx, "baremetal/bandwidth", SUBID=subid)


async def create(
    hub, ctx, metalplan: str, os: str, **kwargs
) -> Tuple[bool, Dict[str, Dict[str, Any]]]:
    r"""
    Create a new bare metal server.
    You will start being billed for this immediately.
    The response only contains the SUBID for the new machine.
    To determine that a server is ready for use, you may poll /v1/baremetal/list?SUBID=<SUBID> and check that the "status" field is set to "active", then test your OS login with SSH (Linux) or RDP (Windows).
    In order to create a server using a snapshot, use os 164 and specify a SNAPSHOTID.

    CLI Example:

    .. code-block:: bash

        idem exec vultr.baremetal.create
    """
    result, status = await hub.exec.vultr.util.query(
        ctx, "baremetal/create", method="POST", metalplan=metalplan, os=os, **kwargs,
    )

    if result:
        subid = status["SUBID"]
        r2, s2 = await hub.exec.vultr.baremetal.server.list(ctx, raw_SUBID=subid)
        # wait for "status" to be "active"
        time_start = 0
        while s2["status"] != "active":
            time_start += hub.OPT.idem.vultr_check_interval
            await asyncio.sleep(hub.OPT.idem.vultr_check_interval)
            r2, s2 = await hub.exec.vultr.baremetal.server.list(ctx, raw_SUBID=subid)
            if (
                hub.OPT.idem.vultr_timeout is not None
                and time_start >= hub.OPT.idem.vultr_timeout
            ):
                hub.log.error(
                    f"Timeout reached while waiting for vm to become active: {subid}"
                )
                break

    return result, status


async def destroy(hub, ctx, subid: int) -> Dict[str, Dict[str, Any]]:
    r"""
    Destroy (delete) a bare metal server. All data will be permanently lost, and the IP address will be released. There is no going back from this call.

    CLI Example:

    .. code-block:: bash

        idem exec vultr.baremetal.destroy
    """
    return await hub.exec.vultr.util.query(
        ctx, "baremetal/destroy", method="POST", SUBID=subid
    )


async def halt(hub, ctx, subid: int) -> Dict[str, Dict[str, Any]]:
    r"""
    Halt a bare metal server.
    This is a hard power off, meaning that the power to the machine is severed.
    The data on the machine will not be modified, and you will still be billed for the machine.
    To completely delete a machine, see v1/baremetal/destroy.

    CLI Example:

    .. code-block:: bash

        idem exec vultr.baremetal.halt
    """
    return await hub.exec.vultr.util.query(
        ctx, "baremetal/halt", method="POST", SUBID=subid
    )


async def label_set(hub, ctx, subid: int, label: str) -> Dict[str, Dict[str, Any]]:
    r"""
    Set the label of a bare metal server.

    CLI Example:

    .. code-block:: bash

        idem exec vultr.baremetal.label new_label subid=00000
    """
    return await hub.exec.vultr.util.query(
        ctx, "baremetal/label_set", method="POST", SUBID=subid, raw_label=label
    )


async def list_(hub, ctx, **kwargs,) -> Dict[str, Dict[str, Any]]:
    r"""
    List all bare metal servers on the current account. This includes both pending and active servers.

    To determine that a server is ready for use, you may poll /v1/baremetal/list?SUBID=<SUBID> and check that the "status" field is set to "active", then test your OS login with SSH (Linux) or RDP (Windows).

    The "status" field represents the status of the subscription. It will be one of: pending | active | suspended | closed.

    If you need to filter the list, review the parameters for this function. Currently, only one filter at a time may be applied (SUBID, tag, label, main_ip).

    CLI Example:

    .. code-block:: bash

        idem exec vultr.baremetal.list
    """
    return await hub.exec.vultr.util.query(ctx, "baremetal/list", **kwargs)


async def reboot(hub, ctx, subid: int) -> Dict[str, Dict[str, Any]]:
    r"""
    Reboot a bare metal server. This is a hard reboot, which means that the server is powered off, then back on.

    CLI Example:

    .. code-block:: bash

        idem exec vultr.baremetal.reboot
    """
    return await hub.exec.vultr.util.query(ctx, "baremetal/reboot", SUBID=subid)


async def reinstall(hub, ctx, subid: int) -> Dict[str, Dict[str, Any]]:
    r"""
    Reinstall the operating system on a bare metal server.
    All data will be permanently lost, but the IP address will remain the same.
    There is no going back from this call.

    CLI Example:

    .. code-block:: bash

        idem exec vultr.baremetal.reinsstall
    """
    return await hub.exec.vultr.util.query(
        ctx, "baremetal/reinstall", method="POST", SUBID=subid
    )


async def tag_set(hub, ctx, subid: int, tag: str) -> Dict[str, Dict[str, Any]]:
    r"""
    Set the tag of a bare metal server.

    CLI Example:

    .. code-block:: bash

        idem exec vultr.baremetal.tag
    """
    return await hub.exec.vultr.util.query(
        ctx, "baremetal/tag_set", method="POST", SUBID=subid, tag=tag
    )
