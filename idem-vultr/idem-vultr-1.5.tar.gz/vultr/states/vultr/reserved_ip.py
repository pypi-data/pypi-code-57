from dict_tools import differ
from typing import Any, Dict

__virtualname__ = "ip"


async def absent(hub, ctx, name: str) -> Dict[str, Any]:
    ret = {
        "name": name,
        "result": True,
        "changes": None,
        "comment": "",
    }

    changes_old = hub.exec.vultr.util.get(
        name, await hub.exec.vultr.ip.list(ctx), ["SUBID", "subnet", "label"]
    )
    if not changes_old:
        ret["comment"] = f"Vultr ip {name} is already absent"
        return ret

    if ctx["test"]:
        ret["comment"] = f"Vultr ip {name} would be deleted"
        return ret

    result = await hub.exec.vultr.ip.delete(ctx, snapshot=changes_old["subnet"])
    ret["result"] = result[0]
    ret["comment"] = result[1].get(
        "VULTR_API_REQUEST_STATUS", f"Deleted vultr ip: {name}"
    )

    changes_new = hub.exec.vultr.util.get(
        name, await hub.exec.vultr.ip.list(ctx), ["SUBID", "subnet", "label"]
    )

    ret["changes"] = differ.deep_diff(changes_old, changes_new)

    return ret


async def present(hub, ctx, name: str, **kwargs) -> Dict[str, Any]:
    ret = {
        "name": name,
        "result": True,
        "changes": None,
        "comment": "",
    }

    changes_old = hub.exec.vultr.util.get(
        name, await hub.exec.vultr.ip.list(ctx), ["SUBID", "subnet", "label"]
    )
    if changes_old:
        ret["comment"] = f"Vultr ip {name} is already present"
        return ret

    if ctx["test"]:
        return ret

    result = await hub.exec.vultr.ip.create(ctx, label=name, **kwargs)
    ret["result"] = result[0]
    ret["comment"] = result[1].get(
        "VULTR_API_REQUEST_STATUS", f"Created vultr ip: {name}"
    )

    changes_new = hub.exec.vultr.util.get(
        name, await hub.exec.vultr.ip.list(ctx), ["SUBID", "subnet", "label"]
    )

    ret["changes"] = differ.deep_diff(changes_old, changes_new)

    return ret
