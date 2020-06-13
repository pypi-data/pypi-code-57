import asyncio
from typing import Any, Dict, Tuple

__virtualname__ = "vm"
__func_alias__ = {
    "destroy": "delete",
    "firewall_group_set": "firewall_group",
    "label_set": "label",
    "list_": "list",
    "tag_set": "tag",
}


async def bandwidth(hub, ctx, subid: int) -> Tuple[bool, Dict[str, Any]]:
    """
    Get the bandwidth used by a virtual machine.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.server.vm.bandwidth
    """
    return await hub.exec.vultr.util.query(ctx, "server/app_change_list", SUBID=subid)


async def create(
    hub, ctx, vps_plan: int, os: str, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    """
    Create a new virtual machine.
    You will start being billed for this immediately.
    The response only contains the SUBID for the new machine.

    To determine that a server is ready for use, you may poll /v1/server/list?SUBID=<SUBID> and check that the "status" field is set to "active", then test your OS login with SSH (Linux) or RDP (Windows).

    In order to create a server using a snapshot, use OSID 164 and specify a snapshot.
    Similarly, to create a server using an ISO use OSID 159 and specify an ISOID.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.server.vm.create
    """
    result, status = await hub.exec.vultr.util.query(
        ctx, "server/create", method="POST", vps_plan=vps_plan, os=os, **kwargs,
    )
    if result:
        subid = status["SUBID"]
        r2, s2 = await hub.exec.vultr.server.vm.list(ctx, subid=subid)
        # wait for "status" to be "active"
        time_start = 0
        while s2["status"] != "active":
            time_start += hub.OPT.idem.vultr_check_interval
            await asyncio.sleep(hub.OPT.idem.vultr_check_interval)
            r2, s2 = await hub.exec.vultr.server.vm.list(ctx, subid=subid)
            if (
                hub.OPT.idem.vultr_timeout is not None
                and time_start >= hub.OPT.idem.vultr_timeout
            ):
                hub.log.error(
                    f"Timeout reached while waiting for vm to become active: {subid}"
                )
                break

    return result, status


async def destroy(hub, ctx, subid: int) -> Tuple[bool, Dict[str, Any]]:
    """
    Destroy (delete) a virtual machine.
    All data will be permanently lost, and the IP address will be released.
    There is no going back from this call.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.server.vm.delete
    """
    return await hub.exec.vultr.util.query(
        ctx, "server/destroy", method="POST", SUBID=subid,
    )


async def firewall_group_set(
    hub, ctx, subid: int, firewall_group: int
) -> Tuple[bool, Dict[str, Any]]:
    """
    Destroy (delete) a virtual machine.
    All data will be permanently lost, and the IP address will be released.
    There is no going back from this call.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.server.vm.firewall_group
    """
    return await hub.exec.vultr.util.query(
        ctx,
        "server/firewall_group_set",
        method="POST",
        SUBID=subid,
        FIREWALLGROUPID=firewall_group,
    )


async def halt(hub, ctx, subid: int) -> Tuple[bool, Dict[str, Any]]:
    """
    Halt a virtual machine.
    This is a hard power off (basically, unplugging the machine).
    The data on the machine will not be modified, and you will still be billed for the machine.
    To completely delete a machine, see v1/server/destroy.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.server.vm.halt
    """
    return await hub.exec.vultr.util.query(
        ctx, "server/halt", method="POST", SUBID=subid,
    )


async def label_set(hub, ctx, subid: int, label: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Set the label of a virtual machine.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.server.vm.label
    """
    return await hub.exec.vultr.util.query(
        ctx, "server/label_set", method="POST", SUBID=subid, raw_label=label
    )


async def list_(hub, ctx, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    """
    List all active or pending virtual machines on the current account.

    To determine that a server is ready for use, you may poll /v1/server/list?SUBID=<SUBID> and check that the "status" field is set to "active", then test your OS login with SSH (Linux) or RDP (Windows).

    The "status" field represents the status of the subscription and will be one of: pending | active | suspended | closed.
    If the status is "active", you can check "power_status" to determine if the VPS is powered on or not.
    When status is "active", you may also use "server_state" for a more detailed status of: none | locked | installingbooting | isomounting | ok.

    The "v6_network", "v6_main_ip", and "v6_network_size" fields are deprecated in favor of "v6_networks".

    The "kvm_url" value will change periodically. It is not advised to cache this value.

    If you need to filter the list, review the parameters for this function.
    Currently, only one filter at a time may be applied (SUBID, tag, label, main_ip).

    CLI Example:

    .. code-block:: bash
        idem exec vultr.server.vm.list
    """
    return await hub.exec.vultr.util.query(ctx, "server/list", **kwargs)


async def neighbors(hub, ctx, subid: int) -> Tuple[bool, Dict[str, Any]]:
    """
    Determine what other subscriptions are hosted on the same physical host as a given subscription.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.server.vm.list
    """
    return await hub.exec.vultr.util.query(ctx, "server/neighbors", SUBID=subid)


async def reboot(hub, ctx, subid: int) -> Tuple[bool, Dict[str, Any]]:
    """
    Reboot a virtual machine. This is a hard reboot (basically, unplugging the machine).

    CLI Example:

    .. code-block:: bash
        idem exec vultr.server.vm.reboot
    """
    return await hub.exec.vultr.util.query(ctx, "server/reboot", SUBID=subid)


async def reinstall(hub, ctx, subid: int, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    """
    Reboot a virtual machine. This is a hard reboot (basically, unplugging the machine).

    CLI Example:

    .. code-block:: bash
        idem exec vultr.server.vm.reinstall
    """
    return await hub.exec.vultr.util.query(
        ctx, "server/reinstall", SUBID=subid, **kwargs
    )


async def start(hub, ctx, subid: int) -> Tuple[bool, Dict[str, Any]]:
    """
    Start a virtual machine. If the machine is already running, it will be restarted.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.server.vm.start
    """
    return await hub.exec.vultr.util.query(
        ctx, "server/start", method="POST", SUBID=subid
    )


async def tag_set(hub, ctx, subid: int, tag: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Set the tag of a virtual machine.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.server.vm.start
    """
    return await hub.exec.vultr.util.query(
        ctx, "server/start", method="POST", SUBID=subid, tag=tag
    )
