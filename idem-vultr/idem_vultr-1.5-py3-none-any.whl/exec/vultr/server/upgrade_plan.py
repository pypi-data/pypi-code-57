from typing import Any, Dict, Tuple

__virtualname__ = "plan"
__func_alias__ = {
    "list_": "list",
}


async def upgrade(hub, ctx, subid: int, vps_plan: int) -> Tuple[bool, Dict[str, Any]]:
    """
    Upgrade the plan of a virtual machine.
    The virtual machine will be rebooted upon a successful upgrade.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.server.vm.plan.upgrade
    """
    return await hub.exec.vultr.util.query(
        ctx, "server/upgrade_plan_list", SUBID=subid, vps_plan=vps_plan
    )


async def list_(hub, ctx, subid: int) -> Tuple[bool, Dict[str, Any]]:
    """
    Retrieve a list of the VPSPLANIDs for which a virtual machine can be upgraded.
    An empty response array means that there are currently no upgrades available.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.server.plan.list
    """
    return await hub.exec.vultr.util.query(ctx, "server/upgrade_plan_list", SUBID=subid)
