from dict_tools import differ
from typing import Any, Dict

__virtualname__ = "script"


async def absent(hub, ctx, name: str) -> Dict[str, Any]:
    ret = {
        "name": name,
        "result": True,
        "changes": None,
        "comment": "",
    }

    changes_old = hub.exec.vultr.util.get(
        name, await hub.exec.vultr.script.list(ctx), ["name", "SCRIPTID", "script"],
    )
    if not changes_old:
        ret["comment"] = f"Vultr startup_script {name} is already absent"
        return ret

    if ctx["test"]:
        ret["comment"] = f"Vultr startup_script {name} would be deleted"
        return ret

    result = await hub.exec.vultr.script.delete(ctx, script=changes_old["SCRIPTID"])
    ret["result"] = result[0]
    ret["comment"] = result[1].get(
        "VULTR_API_REQUEST_STATUS", f"Deleted vultr startup_script: {name}"
    )

    changes_new = hub.exec.vultr.util.get(
        name, await hub.exec.vultr.script.list(ctx), ["name", "SCRIPTID", "script"],
    )

    ret["changes"] = differ.deep_diff(changes_old, changes_new)

    return ret


async def present(hub, ctx, name: str, content: str, pxe: bool) -> Dict[str, Any]:
    ret = {
        "name": name,
        "result": True,
        "changes": None,
        "comment": "",
    }

    changes_old = hub.exec.vultr.util.get(
        name, await hub.exec.vultr.script.list(ctx), ["name", "SCRIPTID", "script"],
    )
    if changes_old:
        ret["comment"] = f"Vultr startup_script {name} is already present"
        return ret

    if ctx["test"]:
        return ret

    result = await hub.exec.vultr.script.create(
        ctx, name=name, content=content, pxe=pxe
    )
    ret["result"] = result[0]
    ret["comment"] = result[1].get(
        "VULTR_API_REQUEST_STATUS", f"Created vultr startup_script: {name}"
    )

    changes_new = hub.exec.vultr.util.get(
        name, await hub.exec.vultr.script.list(ctx), ["name", "SCRIPTID", "script"],
    )

    ret["changes"] = differ.deep_diff(changes_old, changes_new)

    return ret
