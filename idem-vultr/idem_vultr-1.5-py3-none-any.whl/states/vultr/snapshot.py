from dict_tools import differ
from typing import Any, Dict

__func_alias__ = {
    "destroy": "delete",
    "list_": "list",
}


async def absent(hub, ctx, name: str) -> Dict[str, Any]:
    ret = {
        "name": name,
        "result": True,
        "changes": None,
        "comment": "",
    }

    changes_old = hub.exec.vultr.util.get(
        name, await hub.exec.vultr.snapshot.list(ctx), ["description", "SNAPSHOTID"],
    )
    if not changes_old:
        ret["comment"] = f"Vultr snapshot {name} is already absent"
        return ret

    if ctx["test"]:
        ret["comment"] = f"Vultr snapshot {name} would be deleted"
        return ret

    result = await hub.exec.vultr.snapshot.delete(
        ctx, snapshot=changes_old["SNAPSHOTID"]
    )
    ret["result"] = result[0]
    ret["comment"] = result[1].get(
        "VULTR_API_REQUEST_STATUS", f"Deleted vultr snapshot: {name}"
    )

    changes_new = hub.exec.vultr.util.get(
        name, await hub.exec.vultr.snapshot.list(ctx), ["description", "SNAPSHOTID"],
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
        name, await hub.exec.vultr.snapshot.list(ctx), ["description", "SNAPSHOTID"],
    )
    if changes_old:
        ret["comment"] = f"Vultr snapshot {name} is already present"
        return ret

    if ctx["test"]:
        return ret

    result = await hub.exec.vultr.snapshot.create(ctx, subid=name, **kwargs)
    ret["result"] = result[0]
    ret["comment"] = result[1].get(
        "VULTR_API_REQUEST_STATUS", f"Created vultr snapshot: {name}"
    )

    changes_new = hub.exec.vultr.util.get(
        name, await hub.exec.vultr.snapshot.list(ctx), ["description", "SNAPSHOTID"],
    )

    ret["changes"] = differ.deep_diff(changes_old, changes_new)

    return ret
