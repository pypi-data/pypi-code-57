import enum
from typing import Any, Dict, Tuple

__func_alias__ = {
    "availability_": "availability",
    "list_": "list",
}


class Plan(enum.Enum):
    all = "all"
    ssd = "ssd"
    vc2 = "vc2"
    vdc2 = "vdc2"
    dedicated = "dedicated"


async def availability_(hub, ctx, plan_type: str = "all"):
    """
    Retrieve a list of the VPSPLANIDs currently available in this location.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.regions.availability
    """
    if plan_type == "baremetal":
        return await hub.exec.vultr.util.query(ctx, "regions/availability_baremetal")
    else:
        return await hub.exec.vultr.util.query(
            ctx, "regions/availability", type=Plan(plan_type).name
        )


async def list_(hub, ctx, availability: bool = False) -> Tuple[bool, Dict[str, Any]]:
    """
    List all domains associated with the current account.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.regions.list
    """
    return await hub.exec.vultr.util.query(
        ctx, "regions/list", raw_availability="yes" if availability else "no"
    )
