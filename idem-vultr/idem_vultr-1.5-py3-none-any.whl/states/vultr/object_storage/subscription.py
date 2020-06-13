from dict_tools import differ
from typing import Any, Dict


async def absent(hub, ctx, name: str) -> Dict[str, Any]:
    ret = {
        "name": name,
        "result": True,
        "changes": None,
        "comment": "",
    }

    _, changes_old = await hub.exec.vultr.object_storage.subscription.list(
        ctx, label=name
    )
    if not changes_old:
        ret["comment"] = f"Vultr object_storage.subscription {name} is already absent"
        return ret

    if ctx["test"]:
        ret["comment"] = f"Vultr object_storage.subscription {name} would be deleted"
        return ret

    result = await hub.exec.vultr.object_storage.subscription.delete(
        ctx, user_id=changes_old["SUBID"]
    )
    ret["result"] = result[0]
    ret["comment"] = result[1].get(
        "VULTR_API_REQUEST_STATUS", f"Deleted vultr object_storage.subscription: {name}"
    )

    _, changes_new = await hub.exec.vultr.object_storage.subscription.list(
        ctx, label=name
    )

    ret["changes"] = differ.deep_diff(changes_old, changes_new)

    return ret


async def present(hub, ctx, name: str, cluster: str) -> Dict[str, Any]:
    ret = {
        "name": name,
        "result": True,
        "changes": None,
        "comment": "",
    }

    changes_old = await hub.exec.vultr.object_storage.subscription.list(ctx, label=name)
    if changes_old:
        ret["comment"] = f"Vultr instance {name} is already present"
        return ret

    if ctx["test"]:
        return ret

    result = await hub.exec.vultr.object_storage.subscription.create(
        ctx, label=name, cluster=cluster
    )
    ret["result"] = result[0]
    ret["comment"] = result[1].get(
        "VULTR_API_REQUEST_STATUS", f"Created vultr object_storage.subscription: {name}"
    )

    changes_new = await hub.exec.vultr.object_storage.subscription.list(ctx, label=name)

    ret["changes"] = differ.deep_diff(changes_old, changes_new)

    return ret
