import enum
from typing import Any, Dict, Tuple

__func_alias__ = {
    "list_": "list",
}


class Plan(enum.Enum):
    baremetal = "baremetal"
    vc2 = "vc2"
    vc2z = "vc2z"
    vdc2 = "vdc2"


async def list_(hub, ctx, plan: str = None) -> Tuple[bool, Dict[str, Any]]:
    """
    CLI Example:

    .. code-block:: bash
        idem exec vultr.plans.list
    """
    plan_url = "plans/list"
    if plan is not None:
        plan_url += f"_{Plan(plan).name}"
    return await hub.exec.vultr.util.query(ctx, plan_url)
