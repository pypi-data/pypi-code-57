from dict_tools import differ
from typing import Any, Dict, List

__virtualname__ = "user"


async def absent(hub, ctx, name: str) -> Dict[str, Any]:
    ret = {
        "name": name,
        "result": True,
        "changes": None,
        "comment": "",
    }

    changes_old = hub.exec.vultr.util.get(
        name, await hub.exec.vultr.user.list(ctx), ["name", "USERID"]
    )
    if not changes_old:
        ret["comment"] = f"Vultr user {name} is already absent"
        return ret

    if ctx["test"]:
        ret["comment"] = f"Vultr user {name} would be deleted"
        return ret

    result = await hub.exec.vultr.user.delete(ctx, user_id=changes_old["USERID"])
    ret["result"] = result[0]
    ret["comment"] = result[1].get(
        "VULTR_API_REQUEST_STATUS", f"Deleted vultr user: {name}"
    )

    changes_new = hub.exec.vultr.util.get(
        name, await hub.exec.vultr.user.list(ctx), ["name", "USERID"]
    )

    ret["changes"] = differ.deep_diff(changes_old, changes_new)

    return ret


async def present(
    hub, ctx, name: str, password: str, email: str, acls: List[str], **kwargs
) -> Dict[str, Any]:
    ret = {
        "name": name,
        "result": True,
        "changes": None,
        "comment": "",
    }

    changes_old = hub.exec.vultr.util.get(
        name, await hub.exec.vultr.user.list(ctx), ["name", "USERID"]
    )
    if changes_old:
        ret["comment"] = f"Vultr instance {name} is already present"
        return ret

    if ctx["test"]:
        return ret

    result = await hub.exec.vultr.user.create(
        ctx, name=name, password=password, email=email, acls=acls, **kwargs
    )
    ret["result"] = result[0]
    ret["comment"] = result[1].get(
        "VULTR_API_REQUEST_STATUS", f"Created vultr user: {name}"
    )

    changes_new = hub.exec.vultr.util.get(
        name, await hub.exec.vultr.user.list(ctx), ["name", "USERID"]
    )

    ret["changes"] = differ.deep_diff(changes_old, changes_new)

    return ret
