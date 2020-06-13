from dict_tools import differ
from typing import Any, Dict


async def absent(hub, ctx, name: str) -> Dict[str, Any]:
    ret = {
        "name": name,
        "result": True,
        "changes": None,
        "comment": "",
    }

    changes_old = hub.exec.vultr.util.get(
        name, await hub.exec.vultr.server.ipv4.list(ctx), ["SUBID", "ip",]
    )
    if not changes_old:
        ret["comment"] = f"Vultr server.ipv4 {name} is already absent"
        return ret

    if ctx["test"]:
        ret["comment"] = f"Vultr server.ipv4 {name} would be deleted"
        return ret

    result = await hub.exec.vultr.server.ipv4.delete(ctx, subid=changes_old["SUBID"])
    ret["result"] = result[0]
    ret["comment"] = result[1].get(
        "VULTR_API_REQUEST_STATUS", f"Deleted vultr server.ipv4: {name}"
    )

    changes_new = hub.exec.vultr.util.get(
        name, await hub.exec.vultr.server.ipv4.list(ctx), ["SUBID", "ip"]
    )

    ret["changes"] = differ.deep_diff(changes_old, changes_new)

    return ret


async def present(
    hub, ctx, name: str, subid: int, reboot: bool = True
) -> Dict[str, Any]:
    ret = {
        "name": name,
        "result": True,
        "changes": None,
        "comment": "",
    }

    changes_old = hub.exec.vultr.util.get(
        name, await hub.exec.vultr.server.ipv4.list(ctx), ["SUBID", "ip"]
    )
    if changes_old:
        ret["comment"] = f"Vultr server.ipv4 {name} is already present"
        return ret

    if ctx["test"]:
        return ret

    result = await hub.exec.vultr.server.ipv4.create(ctx, subid=subid, reboot=reboot)
    ret["result"] = result[0]
    ret["comment"] = result[1].get(
        "VULTR_API_REQUEST_STATUS", f"Created vultr server.ipv4: {name}"
    )

    changes_new = hub.exec.vultr.util.get(
        name, await hub.exec.vultr.server.ipv4.list(ctx), ["SUBID", "ip"]
    )

    ret["changes"] = differ.deep_diff(changes_old, changes_new)

    return ret
