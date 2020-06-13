from typing import Any, Dict, Tuple

__func_alias__ = {
    "list_": "list",
}


async def create(hub, ctx, domain: str, ip: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Create a domain name in DNS.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.dns.domain.create
    """
    return await hub.exec.vultr.util.query(
        ctx, "dns/create_domain", method="POST", domain=domain, serverip=ip
    )


async def delete(hub, ctx, domain: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Delete a domain name and all associated records.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.dns.domain.delete
    """
    return await hub.exec.vultr.util.query(
        ctx, "dns/delete_domain", method="POST", domain=domain
    )


async def list_(hub, ctx) -> Tuple[bool, Dict[str, Any]]:
    """
    List all domains associated with the current account.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.dns.domain.list
    """
    return await hub.exec.vultr.util.query(ctx, "dns/list")
