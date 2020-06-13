from dict_tools import differ
from typing import Any, Dict

__virtualname__ = "iso"


async def absent(hub, ctx, name: str) -> Dict[str, Any]:
    ret = {
        "name": name,
        "result": True,
        "changes": None,
        "comment": "",
    }

    changes_old = hub.exec.vultr.util.get(
        name, await hub.exec.vultr.iso.list(ctx), ["ISOID", "filename"]
    )
    if not changes_old:
        ret["comment"] = f"Vultr iso {name} is already absent"
        return ret

    if ctx["test"]:
        ret["comment"] = f"Vultr iso {name} would be deleted"
        return ret

    result = await hub.exec.vultr.iso.delete(ctx, iso=changes_old["ISOID"])
    ret["result"] = result[0]
    ret["comment"] = result[1].get(
        "VULTR_API_REQUEST_STATUS", f"Deleted vultr iso: {name}"
    )

    changes_new = hub.exec.vultr.util.get(
        name, await hub.exec.vultr.iso.list(ctx), ["ISOID", "filename"]
    )

    ret["changes"] = differ.deep_diff(changes_old, changes_new)

    return ret


async def present(hub, ctx, name: str, url: str) -> Dict[str, Any]:
    ret = {
        "name": name,
        "result": True,
        "changes": None,
        "comment": "",
    }

    changes_old = hub.exec.vultr.util.get(
        name, await hub.exec.vultr.iso.list(ctx), ["ISOID", "filename"]
    )
    if changes_old:
        ret["comment"] = f"Vultr iso {name} is already present"
        return ret

    if ctx["test"]:
        return ret

    result = await hub.exec.vultr.iso.create(ctx, url=url)
    ret["result"] = result[0]
    ret["comment"] = result[1].get(
        "VULTR_API_REQUEST_STATUS", f"Created vultr iso: {name}"
    )

    changes_new = hub.exec.vultr.util.get(
        name, await hub.exec.vultr.iso.list(ctx), ["ISOID", "filename"]
    )

    ret["changes"] = differ.deep_diff(changes_old, changes_new)

    return ret
