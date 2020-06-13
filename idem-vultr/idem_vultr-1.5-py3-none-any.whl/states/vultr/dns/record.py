from dict_tools import differ
from typing import Any, Dict


async def absent(hub, ctx, name: str, domain: str) -> Dict[str, Any]:
    ret = {
        "name": name,
        "result": True,
        "changes": None,
        "comment": "",
    }

    changes_old = hub.exec.vultr.util.get(
        name, await hub.exec.vultr.dns.record.list(ctx), ["name", "RECORDID"]
    )
    if not changes_old:
        ret["comment"] = f"Vultr dns.record {name} is already absent"
        return ret

    if ctx["test"]:
        ret["comment"] = f"Vultr dns.record {name} would be deleted"
        return ret

    result = await hub.exec.vultr.dns.record.delete(
        ctx, recordid=changes_old["RECORDID"], domain=domain
    )
    ret["result"] = result[0]
    ret["comment"] = result[1].get(
        "VULTR_API_REQUEST_STATUS", f"Deleted vultr dns.record: {name}"
    )

    changes_new = hub.exec.vultr.util.get(
        name, await hub.exec.vultr.dns.record.list(ctx), ["name", "RECORDID"]
    )

    ret["changes"] = differ.deep_diff(changes_old, changes_new)

    return ret


async def present(
    hub, ctx, name: str, domain: str, type_: str, data: str, **kwargs
) -> Dict[str, Any]:
    ret = {
        "name": name,
        "result": True,
        "changes": None,
        "comment": "",
    }

    changes_old = hub.exec.vultr.util.get(
        name, await hub.exec.vultr.dns.record.list(ctx), ["name", "RECORDID"]
    )
    if changes_old:
        ret["comment"] = f"Vultr instance {name} is already present"
        return ret

    if ctx["test"]:
        return ret

    result = await hub.exec.vultr.dns.record.create(
        ctx, name=name, domain=domain, type_=type_, data=data, **kwargs
    )
    ret["result"] = result[0]
    ret["comment"] = result[1].get(
        "VULTR_API_REQUEST_STATUS", f"Created vultr dns.record: {name}"
    )

    changes_new = hub.exec.vultr.util.get(
        name, await hub.exec.vultr.dns.record.list(ctx), ["name", "RECORDID"]
    )

    ret["changes"] = differ.deep_diff(changes_old, changes_new)

    return ret
