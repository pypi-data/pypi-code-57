from dict_tools import differ
from typing import Any, Dict


async def absent(hub, ctx, name: str, firewall_group: str) -> Dict[str, Any]:
    ret = {
        "name": name,
        "result": True,
        "changes": None,
        "comment": "",
    }

    changes_old = hub.exec.vultr.util.get(
        name, await hub.exec.vultr.firewall.rule.list(ctx), ["rulenumber", "notes"]
    )
    if not changes_old:
        ret["comment"] = f"Vultr firewall.rule {name} is already absent"
        return ret

    if ctx["test"]:
        ret["comment"] = f"Vultr firewall.rule {name} would be deleted"
        return ret

    result = await hub.exec.vultr.firewall.rule.delete(
        ctx, firewall_group=firewall_group, rule_number=changes_old["rulenumber"]
    )
    ret["result"] = result[0]
    ret["comment"] = result[1].get(
        "VULTR_API_REQUEST_STATUS", f"Deleted vultr user: {name}"
    )

    changes_new = hub.exec.vultr.util.get(
        name, await hub.exec.vultr.firewall.rule.list(ctx), ["rulenumber", "notes"]
    )

    ret["changes"] = differ.deep_diff(changes_old, changes_new)

    return ret


async def present(
    hub,
    ctx,
    name: str,
    firewall_group: str,
    ip_type: int,
    protocol: str,
    subnet: str,
    subnet_size: int,
    **kwargs,
) -> Dict[str, Any]:
    ret = {
        "name": name,
        "result": True,
        "changes": None,
        "comment": "",
    }

    changes_old = hub.exec.vultr.util.get(
        name, await hub.exec.vultr.firewall.rule.list(ctx), ["rulenumber", "notes"]
    )
    if changes_old:
        ret["comment"] = f"Vultr firewall.rule {name} is already present"
        return ret

    if ctx["test"]:
        return ret

    result = await hub.exec.vultr.firewall.rule.create(
        ctx,
        notes=name,
        firewall_group=firewall_group,
        ip_type=ip_type,
        protocol=protocol,
        subnet=subnet,
        subnet_size=subnet_size,
        **kwargs,
    )
    ret["result"] = result[0]
    ret["comment"] = result[1].get(
        "VULTR_API_REQUEST_STATUS", f"Created vultr firewall.rule: {name}"
    )

    changes_new = hub.exec.vultr.util.get(
        name, await hub.exec.vultr.firewall.rule.list(ctx), ["rulenumber", "notes"]
    )

    ret["changes"] = differ.deep_diff(changes_old, changes_new)

    return ret
