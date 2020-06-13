from dict_tools import differ
from typing import Any, Dict

__virtualname__ = "block"


async def absent(hub, ctx, name: str) -> Dict[str, Any]:
    ret = {
        "name": name,
        "result": True,
        "changes": None,
        "comment": "",
    }

    changes_old = hub.exec.vultr.util.get(
        name, await hub.exec.vultr.block.list(ctx), ["SUBID", "label"]
    )
    if not changes_old:
        ret["comment"] = f"Vultr block {name} is already absent"
        return ret

    if ctx["test"]:
        ret["comment"] = f"Vultr block {name} would be deleted"
        return ret

    result = await hub.exec.vultr.block.delete(ctx, subid=changes_old["SUBID"])
    ret["result"] = result[0]
    ret["comment"] = result[1].get(
        "VULTR_API_REQUEST_STATUS", f"Deleted vultr block: {name}"
    )

    changes_new = hub.exec.vultr.util.get(
        name, await hub.exec.vultr.block.list(ctx), ["SUBID", "label"]
    )

    ret["changes"] = differ.deep_diff(changes_old, changes_new)

    return ret


async def present(hub, ctx, name: str, subid: int, size_gb: int) -> Dict[str, Any]:
    ret = {
        "name": name,
        "result": True,
        "changes": None,
        "comment": "",
    }

    changes_old = hub.exec.vultr.util.get(
        name, await hub.exec.vultr.block.list(ctx), ["SUBID", "label"]
    )
    if changes_old:
        ret["comment"] = f"Vultr block {name} is already present"
        return ret

    if ctx["test"]:
        return ret

    result = await hub.exec.vultr.block.create(
        ctx, subid=subid, label=name, size_gb=size_gb
    )
    ret["result"] = result[0]
    ret["comment"] = result[1].get(
        "VULTR_API_REQUEST_STATUS", f"Created vultr block: {name}"
    )

    changes_new = hub.exec.vultr.util.get(
        name, await hub.exec.vultr.block.list(ctx), ["SUBID", "label"]
    )

    ret["changes"] = differ.deep_diff(changes_old, changes_new)

    return ret
