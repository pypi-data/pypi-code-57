from dict_tools import differ
from typing import Any, Dict


async def absent(hub, ctx, name: str) -> Dict[str, Any]:
    ret = {
        "name": name,
        "result": True,
        "changes": None,
        "comment": "",
    }

    changes_old = (await hub.exec.vultr.network.list(ctx)).get(name)

    if not changes_old:
        ret["comment"] = f"Vultr network {name} is already absent"
        return ret

    if ctx["test"]:
        ret["comment"] = f"Vultr network {name} would be deleted"
        return ret

    result = await hub.exec.vultr.network.delete(ctx, network=changes_old["network"])
    ret["result"] = result[0]
    ret["comment"] = result[1].get(
        "VULTR_API_REQUEST_STATUS", f"Deleted vultr network: {name}"
    )

    changes_new = (await hub.exec.vultr.network.list(ctx)).get(name)

    ret["changes"] = differ.deep_diff(changes_old, changes_new)

    return ret


async def present(hub, ctx, name: str, **kwargs) -> Dict[str, Any]:
    ret = {
        "name": name,
        "result": True,
        "changes": None,
        "comment": "",
    }

    changes_old = (await hub.exec.vultr.network.list(ctx)).get(name)

    if changes_old:
        ret["comment"] = f"Vultr network {name} is already present"
        return ret

    if ctx["test"]:
        return ret

    result = await hub.exec.vultr.network.create(ctx, description=name, **kwargs)
    ret["result"] = result[0]
    ret["comment"] = result[1].get(
        "VULTR_API_REQUEST_STATUS", f"Created vultr network: {name}"
    )

    changes_new = (await hub.exec.vultr.network.list(ctx)).get(name)

    ret["changes"] = differ.deep_diff(changes_old, changes_new)

    return ret
